from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.user import UserCreate


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()


def create_user(
    db: Session,
    user_data: UserCreate,
    hashed_password: str,
    role: UserRole = UserRole.user,
) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
