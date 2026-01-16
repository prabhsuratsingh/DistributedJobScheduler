from time import sleep
from app.database.db import SessionLocal
from app.models.job import Job
from app.models.job_status import JobStatus


def send_mail(job_id, payload):
    db = SessionLocal()

    try:
        sleep(1000)
        
        db.query(Job).filter(Job.id == job_id).update({
            Job.remarks: "Job done successfully",
            Job.status: JobStatus.COMPLETED
        })
    except Exception as e:
        db.query(Job).filter(Job.id == job_id).update({
            Job.remarks: f"Job failed with error {str(e)}",
            Job.status: JobStatus.FAILED
        })
    
    db.commit()