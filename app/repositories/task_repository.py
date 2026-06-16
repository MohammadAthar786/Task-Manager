from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    task = Task(**task_data.model_dump(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def get_task_by_owner(db: Session, task_id: int, owner_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def get_tasks_by_owner(db: Session, owner_id: int) -> list[Task]:
    return db.query(Task).filter(Task.owner_id == owner_id).order_by(Task.id).all()


def get_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.id).all()


def update_task(db: Session, task: Task, task_data: TaskUpdate) -> Task:
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
