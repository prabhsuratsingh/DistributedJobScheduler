import uuid
from sqlalchemy import Column, DateTime, Integer, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base
from app.models.job_status import JobStatus


class JobRuns(Base):
    __tablename__ = "job_runs"

    run_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), nullable=False)
    attempt = Column(Integer, nullable=False, default=0)
    status = Column(SQLEnum(JobStatus, name="job_status_enum"), nullable=False, default=JobStatus.PENDING)
    worker_id = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=False)
    error = Column(String, nullable=True)
