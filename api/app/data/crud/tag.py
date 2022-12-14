import sqlalchemy as sa
from app.data.base import Base, BaseRead
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Tag(Base):
    campaign_id = sa.Column(
        sa.Integer, sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )

    name = sa.Column(sa.String, nullable=False)

    __table_args__ = tuple(sa.UniqueConstraint(campaign_id, name))


class TagCreate(BaseModel):
    name: str


class TagRead(BaseRead):
    name: str


class TagUpdate(BaseModel):
    name: str


def create(c_id: int | sa.Column, t: TagCreate, db: Session) -> Tag:
    new_t = Tag(campaign_id=c_id, **t.dict())  # type: ignore
    db.add(new_t)

    db.commit()
    db.refresh(new_t)

    return new_t


def read(id: int | sa.Column, db: Session) -> Tag | None:
    return db.query(Tag).filter(Tag.id == id).first()


def read_all_by_campaign(
    c_id: int | sa.Column, limit: int, offset: int, db: Session
) -> list[Tag]:
    return (
        db.query(Tag).filter(Tag.campaign_id == c_id).limit(limit).offset(offset).all()
    )


def read_all(limit: int, offset: int, db: Session) -> list[Tag]:
    return db.query(Tag).limit(limit).offset(offset).all()


def update(id: int | sa.Column, t: TagUpdate, db: Session) -> None:
    db.query(Tag).filter(Tag.id == id).update(t.dict(exclude_unset=True))

    db.commit()


def delete(id: int | sa.Column, db: Session) -> None:
    db.query(Tag).filter(Tag.id == id).delete()

    db.commit()
