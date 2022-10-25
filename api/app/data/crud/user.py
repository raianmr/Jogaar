from app.data.base import Base, BaseRead
from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, Column, String, text
from sqlalchemy.orm import Session


class User(Base):
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    about = Column(String)
    contact = Column(String)
    address = Column(String)

    moderator = Column(Boolean, server_default=text("False"), nullable=False)
    banned = Column(Boolean, server_default=text("False"), nullable=False)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(BaseRead):
    name: str
    email: EmailStr
    about: str | None
    contact: str | None
    address: str | None
    moderator: bool
    banned: bool


class UserUpdate(BaseModel):
    name: str | None
    email: EmailStr | None
    password: str | None
    about: str | None
    contact: str | None
    address: str | None


def create(u: UserCreate, db: Session) -> User:
    new_u = User(**u.dict())  # type: ignore
    db.add(new_u)

    db.commit()
    db.refresh(new_u)

    return new_u


def read(id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == id).first()


def read_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


def read_all(limit: int, offset: int, db: Session) -> list[User]:
    return db.query(User).limit(limit).offset(offset).all()


def update(id: int, u: UserUpdate, db: Session) -> None:
    db.query(User).filter(User.id == id).update(u.dict(exclude_unset=True))

    db.commit()


def delete(id: int, db: Session) -> None:
    db.query(User).filter(User.id == id).delete()

    db.commit()
