from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.create_job import CreateJob


def create_new_job(db: Session, jd: CreateJob):
    job = Job(
        id = uuid4(),
        job_type= jd.job_type,
        payload=jd.payload,
        schedule_time=jd.schedule_time,
        cron=jd.cron,
        max_retries = jd.max_retries
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job

def get_status_by_id(db: Session, id: UUID):
    resp = db.query(Job).filter(Job.id == id).first()
    return resp

def get_all_status(db: Session):
    return (
        db.query(Job).all()
    )