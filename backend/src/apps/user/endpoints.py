from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from backend.src.apps.user.schemas import UserSchema, UserUpdate
from backend.src.base.crud import CRUDBase
from backend.src.exceptions.model import ErrorResponseModel
from backend.src.models import User
from backend.src.operations.deps import get_db, get_current_active_user

router_user = APIRouter()


@router_user.patch(
    "/users",
    summary="Изменение информации о пользователе",
    response_model=UserUpdate,
)
async def change_data_user(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
        update_user_data: Annotated[UserUpdate, Body()],
        db: Session = Depends(get_db)
):
    """
    Здесь пользователь может изменить сови данные
    :return:
    """
    if current_user.first_name == update_user_data.first_name and \
            current_user.last_name == update_user_data.last_name:
        raise ErrorResponseModel(code=401, message="Вы не изменили поля")
    user = CRUDBase(model=User)
    user_update = user.update(
        db=db,
        obj_in=update_user_data,
        db_obj=current_user
    )
    return user_update
