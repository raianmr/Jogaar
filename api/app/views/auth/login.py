from app.core import security
from app.data.crud import user
from app.data.session import get_db
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", response_model=security.Token)
async def user_login(
    creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    existing_u = user.read_by_email(creds.username, db)

    if existing_u is None:
        raise security.UserNotFoundErr

    if not security.verify_password(creds.password, existing_u.password):
        raise security.AuthenticatingErr

    access_token = security.create_access_token(data={"user_id": existing_u.id})

    return security.Token(
        access_token=access_token,
        token_type="bearer",
        access_level=existing_u.access_level,  # type: ignore
    )


# TODO implement elevated logins
@router.post("/login/super", response_model=security.Token)
async def super_login(
    creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    existing_u = user.read_by_email(creds.username, db)

    if existing_u is None:
        raise security.UserNotFoundErr

    if not security.verify_password(creds.password, existing_u.password):
        raise security.AuthenticatingErr

    if not security.is_super(existing_u):
        raise security.NotAllowedErr

    access_token = security.create_access_token(data={"user_id": existing_u.id})

    return security.Token(
        access_token=access_token,
        token_type="bearer",
        access_level=existing_u.access_level,  # type: ignore
    )
