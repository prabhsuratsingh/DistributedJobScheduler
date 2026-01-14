import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import db
from app.database.crud import create_new_job, get_all_status, get_status_by_id
from app.schemas.create_job import CreateJob, CreateJobPayload

router = APIRouter(prefix="/job", tags=["jobs"])

@router.post("/create")
def create_job(
    data: CreateJobPayload,
    db: Session = Depends(db.get_db)
):
    try:
        job = CreateJob(
            job_type=data.job_type,
            payload=data.payload,
            schedule_time=data.schedule_time,
            cron = data.cron,
            max_retries= data.max_retries
        )

        resp = create_new_job(db, job)

        return {
            "message": "job created!",
            "job": resp
        }
    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e)
            }
        )


@router.get("/status/all")
def get_all_jobs_status(db: Session = Depends(db.get_db)):
    try:
        resp = get_all_status(db)

        return {
            "jobs": [
                {
                    "id": job.id,
                    "status": job.status
                }

                for job in resp
            ]
        }
    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e)
            }
        )

@router.get("/status/{id}")
def get_job_status(id: str, db: Session = Depends(db.get_db)):
    try:
        resp = get_status_by_id(db, id)
        return {
            "job_id": resp.id,
            "status": resp.status
        }
    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e)
            }
        )
