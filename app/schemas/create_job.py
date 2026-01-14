from datetime import datetime
from pydantic import BaseModel


class CreateJobPayload(BaseModel):
    job_type: str
    payload: dict
    schedule_time: datetime
    cron: str | None
    max_retries: int

class CreateJob(BaseModel):
    job_type: str
    payload: dict
    schedule_time: datetime
    cron: str | None
    max_retries: int