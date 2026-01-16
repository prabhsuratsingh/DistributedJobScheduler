from enum import Enum

class JobStatus(Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    CREATED = "created"
    ENQUEUED = "enqueued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    COMPLETED = "completed" 