from app.data.auth import user
from app.data.auth.user import User, UserCreate, UserRead, UserUpdate
from app.data.session import get_db
from app.logic.auth.login import hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

# TODO access guards


router = APIRouter()


class EmailConflictErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="user with given email already exists",
        )


class UserNotFoundErr(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user with given id was not found",
        )


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(u: UserCreate, db: Session = Depends(get_db)) -> User:
    try:
        u.password = hash(u.password)
        new_u = user.create(u, db)

    except IntegrityError:
        raise EmailConflictErr

    return new_u


@router.put("/users/{id}", response_model=UserRead)
async def update_user(id: int, u: UserUpdate, db: Session = Depends(get_db)) -> User:
    existing_u = user.read(id, db)

    if not existing_u:
        raise UserNotFoundErr

    try:
        user.update(id, u, db)
        updated_u = user.read(id, db)

    except IntegrityError:
        raise EmailConflictErr

    return updated_u  # type: ignore


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)) -> None:
    existing_u = user.read(id, db)

    if not existing_u:
        raise UserNotFoundErr

    user.delete(id, db)


@router.get("/users/{id}", response_model=UserRead)
async def read_user(id: int, db: Session = Depends(get_db)) -> User:
    existing_u = user.read(id, db)

    if not existing_u:
        raise UserNotFoundErr

    return existing_u


@router.get("/users", response_model=list[UserRead])
async def read_users(
    limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
) -> list[User]:
    all_u = user.read_all(limit, offset, db)

    return all_u
