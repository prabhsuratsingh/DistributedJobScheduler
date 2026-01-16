from datetime import datetime
from time import sleep
from typing import List
from uuid import uuid4

from app.core.queue import enqueue_job
from app.database.db import SessionLocal
from app.models.job import Job
from app.models.job_run import JobRuns
from app.models.job_status import JobStatus


def scheduler():
    print("Scheduler Running")

    while True:
        db = SessionLocal()
        created_runs: List[JobRuns] = []

        try:
            with db.begin():
                jobs = db.query(Job).filter(
                    Job.status == JobStatus.PENDING,
                    Job.schedule_time <= datetime.now()
                ).order_by(Job.schedule_time).limit(100).with_for_update(skip_locked=True)
                
                for job in jobs:
                    job_run = JobRuns(
                        run_id=uuid4(),
                        job_id=job.id,
                        status=JobStatus.ENQUEUED,
                    )

                    db.add(job_run)
                    created_runs.append(job_run)
                    db.query(Job).filter(Job.id == job.id).update({Job.status: JobStatus.SCHEDULED})
            
            for run in created_runs:
                try:
                    print("Scheduler: attempting to enqueue", run.run_id)
                    enqueue_job(run.run_id)

                except:
                    db.query(JobRuns).filter(JobRuns.run_id == run.run_id).update({
                        JobRuns.status : JobStatus.CREATED
                    })
            
        finally:
            db.close()

        sleep(10)