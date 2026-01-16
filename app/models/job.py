import uuid
from sqlalchemy import Column, DateTime, Integer, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database.base import Base
from app.models.job_status import JobStatus

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    schedule_time = Column(DateTime(timezone=True), nullable=False)
    cron = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    max_retries = Column(Integer, nullable=False)
    status = Column(SQLEnum(JobStatus, name="job_status_enum"), nullable=False, default=JobStatus.PENDING)



