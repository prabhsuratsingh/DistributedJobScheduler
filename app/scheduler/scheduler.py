from datetime import datetime
from time import sleep
from uuid import uuid4

from app.database.db import SessionLocal
from app.models.job import Job
from app.models.job_run import JobRuns
from app.models.job_status import JobStatus


def scheduler():
    db = SessionLocal()

    while True:
        created_runs = []

        with db.begin():
            jobs = db.query(Job).filter(
                Job.status == JobStatus.PENDING,
                Job.schedule_time <= datetime.now()
            ).order_by(Job.schedule_time).limit(100).with_for_update(skip_locked=True)
            
            for job in jobs:
                job_run = JobRuns(
                    run_id=uuid4(),
                    job_id=job.id,
                    status=JobStatus.CREATED,
                )

                db.add(job_run)
                created_runs.append(job_run)
                db.query(Job).filter(Job.id == job.id).update(Job.status == JobStatus.SCHEDULED)
        
        for run in created_runs:
            try:
                updated = db.query(JobRuns).filter(
                        JobRuns.run_id == run.run_id, 
                        JobRuns.status == JobStatus.CREATED
                    ).update({
                        JobRuns.status : JobStatus.ENQUEUED
                    })
                if updated == 1:
                    #push run id to redis queue
                    pass
                else:
                    continue

            except:
                db.query(JobRuns).filter(JobRuns.run_id == run.run_id).update({
                    JobRuns.status : JobStatus.CREATED
                })
        
        job_runs = db.query(JobRuns).filter(
            JobRuns.status == JobStatus.CREATED,
        ).with_for_update(skip_locked=True)

        for jr in job_runs:
            try:
                updated = db.query(JobRuns).filter(
                        JobRuns.run_id == jr.run_id, 
                        JobRuns.status == JobStatus.CREATED
                    ).update({
                        JobRuns.status : JobStatus.ENQUEUED
                    })
                if updated == 1:
                    #push run id to redis queue
                    pass
                else:
                    continue
            except:
                db.query(JobRuns).filter(JobRuns.run_id == jr.run_id).update({
                    JobRuns.status : JobStatus.CREATED
                })

        sleep(500)