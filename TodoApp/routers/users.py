from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..models import Users
from starlette import status
from ..database import db_dependency
from ..data_models import UserVerification, PhoneRequest
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_model


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.commit()


@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(
    user: user_dependency, db: db_dependency, phone_request: PhoneRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.phone_number = phone_request.phone_number

    db.commit()
