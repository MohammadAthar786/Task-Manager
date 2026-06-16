from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate


def create_user_task(db: Session, task_data: TaskCreate, current_user: User):
    return task_repository.create_task(db, task_data, current_user.id)


def get_current_user_tasks(db: Session, current_user: User):
    return task_repository.get_tasks_by_owner(db, current_user.id)


def get_current_user_task(db: Session, task_id: int, current_user: User):
    task = task_repository.get_task_by_owner(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


def update_current_user_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User,
):
    task = get_current_user_task(db, task_id, current_user)
    return task_repository.update_task(db, task, task_data)


def delete_current_user_task(db: Session, task_id: int, current_user: User) -> None:
    task = get_current_user_task(db, task_id, current_user)
    task_repository.delete_task(db, task)
