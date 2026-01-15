from enum import Enum

class JobStatus(Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    CREATED = "created"
    ENQUEUED = "enqueued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"