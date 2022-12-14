from app.core import security, utils
from app.data.crud import reply
from app.data.crud.reply import Reply, ReplyCreate, ReplyRead, ReplyUpdate
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/updates/{up_id}/replies",
    status_code=status.HTTP_201_CREATED,
    response_model=ReplyRead,
)
async def create_reply(
    up_id: int,
    r: ReplyCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> Reply:
    existing_up = utils.get_existing_update(up_id, db)

    try:
        new_r = reply.create(curr_u.id, existing_up.id, r, db)

    except IntegrityError:
        raise utils.MiscConflictErr

    return new_r


@router.put("/replies/{r_id}", response_model=ReplyRead)
async def update_reply(
    r_id: int,
    r: ReplyUpdate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> Reply | None:
    existing_r = utils.get_existing_reply(r_id, db)

    if not security.has_access_over(existing_r, curr_u):
        raise security.NotAllowedErr

    try:
        reply.update(existing_r.id, r, db)
        updated_r = reply.read(existing_r.id, db)

    except IntegrityError:
        raise utils.MiscConflictErr

    return updated_r


@router.delete(
    "/replies/{r_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reply(
    r_id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(security.get_current_valid_user),
) -> None:
    existing_r = utils.get_existing_reply(r_id, db)

    if not security.has_access_over(existing_r, curr_u):
        raise security.NotAllowedErr

    reply.delete(r_id, db)


@router.get("replies/{r_id}", response_model=list[ReplyRead])
async def read_reply(
    r_id: int,
    db: Session = Depends(get_db),
) -> Reply:
    existing_r = utils.get_existing_reply(r_id, db)

    return existing_r


@router.get("/updates/{up_id}/replies", response_model=list[ReplyRead])
async def read_replies_by_update(
    up_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[Reply]:
    all_r_by_c = reply.read_all_by_update(up_id, limit, offset, db)

    return all_r_by_c
