from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, hash_password, verify_password
from app.repositories import user_repository
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate


def register_user(db: Session, user_data: UserCreate):
    existing_user = user_repository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    hashed_password = hash_password(user_data.password)
    return user_repository.create_user(db, user_data, hashed_password)


def authenticate_user(db: Session, login_data: LoginRequest) -> Token:
    user = user_repository.get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)
