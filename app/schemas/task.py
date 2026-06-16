from datetime import datetime

from pydantic import BaseModel

from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.pending


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
