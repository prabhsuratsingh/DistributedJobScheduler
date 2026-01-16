from datetime import datetime
import socket
from uuid import UUID

from app.core.queue import dequeue_job, enqueue_job
from app.database.db import SessionLocal
from app.jobs.registry import JOB_REGISTRY
from app.models.job import Job
from app.models.job_run import JobRuns
from app.models.job_status import JobStatus

WORKER_ID = socket.gethostname()

def worker():
    print("Worker Running")

    while True:
        try:
            print("Before worker dequeue")
            run_id_raw = dequeue_job()
            print("After worker dequeue")

            run_id = UUID(run_id_raw)

            print("[WORKER] dequeued run_id:", run_id, type(run_id))
            db = SessionLocal()

            updated = db.query(JobRuns).filter(
                JobRuns.run_id == run_id,
                JobRuns.status == JobStatus.ENQUEUED
            ).update({
                JobRuns.status: JobStatus.RUNNING,
                JobRuns.worker_id: WORKER_ID,
                JobRuns.started_at: datetime.now()
            }, synchronize_session=False)
            print("[WORKER] update result:", updated)

            db.commit()

            if updated != 1:
                print("[WORKER] claim failed, re-enqueueing", run_id)
                enqueue_job(run_id)
                continue


            job, run = db.query(Job, JobRuns).join(
                JobRuns, Job.id == JobRuns.job_id
            ).filter(JobRuns.run_id == run_id).one()

            job_func = JOB_REGISTRY.get(job.job_type)
            
            job_func(job.id, job.payload)

            db.query(JobRuns).filter(
                JobRuns.run_id == run_id
            ).update({
                JobRuns.status: JobStatus.SUCCESS,
                JobRuns.finished_at: datetime.now()
            })
        
        except Exception as e:
            if run.attempt + 1 >= job.max_retries:
                db.query(JobRuns).filter(
                    JobRuns.run_id == run_id
                ).update({
                    JobRuns.status: JobStatus.FAILED,
                    JobRuns.error: str(e),
                    JobRuns.finished_at: datetime.now()
                })

                db.query(Job).filter(Job.id == job.id).update({
                    Job.remarks: f"Max retries reached, Error: {str(e)}",
                    Job.status: JobStatus.FAILED
                })
            else:
                enqueue_job(run_id)

                db.query(JobRuns).filter(
                    JobRuns.run_id == run_id
                ).update({
                    JobRuns.attempt: run.attempt + 1,
                    JobRuns.status: JobStatus.ENQUEUED,
                    JobRuns.error: str(e)
                })

        
        db.commit()
