from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database import get_db
from app.models.user import User
from app.repositories.task_repository import get_all_tasks
from app.repositories.user_repository import get_all_users
from app.schemas.task import TaskResponse
from app.schemas.user import UserResponse


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserResponse])
def read_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return get_all_users(db)


@router.get("/tasks", response_model=list[TaskResponse])
def read_all_tasks(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return get_all_tasks(db)
