from app.core.campaigning import CampaignNotFoundErr, MiscConflictErr
from app.core.security import NotAllowedErr, get_current_valid_user
from app.data.crud import campaign
from app.data.crud.campaign import (
    Campaign,
    CampaignCreate,
    CampaignRead,
    CampaignUpdate,
)
from app.data.crud.user import User
from app.data.session import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/campaigns", status_code=status.HTTP_201_CREATED, response_model=CampaignRead
)
async def create_campaign(
    c: CampaignCreate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Campaign:
    try:
        new_c = campaign.create(curr_u.id, c, db)  # type: ignore

    except IntegrityError:
        raise MiscConflictErr

    return new_c


@router.put("/campaigns/{id}", response_model=CampaignRead)
async def update_campaign(
    id: int,
    c: CampaignUpdate,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> Campaign | None:
    existing_c = campaign.read(id, db)

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    try:
        campaign.update(id, c, db)
        updated_c = campaign.read(id, db)

    except IntegrityError:
        raise MiscConflictErr

    return updated_c


@router.delete("/campaigns/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    id: int,
    db: Session = Depends(get_db),
    curr_u: User = Depends(get_current_valid_user),
) -> None:
    existing_c = campaign.read(id, db)

    if not existing_c:
        raise CampaignNotFoundErr

    if existing_c.campaigner_id != curr_u.id:
        raise NotAllowedErr

    campaign.delete(id, db)


@router.get("/campaigns/{id}", response_model=CampaignRead)
async def read_campaign(id: int, db: Session = Depends(get_db)) -> Campaign:
    existing_c = campaign.read(id, db)

    if not existing_c:
        raise CampaignNotFoundErr

    return existing_c


@router.get("/campaigns", response_model=list[CampaignRead])
async def read_campaigns(
    limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
) -> list[Campaign]:
    all_c = campaign.read_all(limit, offset, db)

    return all_c


@router.get("/users/{u_id}/campaigns", response_model=list[CampaignRead])
async def read_campaigns_by_user(
    u_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
) -> list[Campaign]:
    all_c_by_u = campaign.read_all_by_user(u_id, limit, offset, db)

    return all_c_by_u