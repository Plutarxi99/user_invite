import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.src.apps.register.crud import create_user, add_in_referal_program
from backend.src.apps.register.schemas import UserCreateModel, UserCreateReferalModel
from backend.src.apps.user.crud import get_user
from backend.src.apps.user.schemas import UserCreate, UserBase, UserIsActiveModel
from backend.src.exceptions.model import ErrorResponseModel
from backend.src.operations.deps import get_db, decode_referer_cod, check_data_ref_cod
from backend.src.services.clearbit.src import write_add_info_user

router_register = APIRouter(
    # dependencies=[
    #     Depends(check_data_ref_cod)
    # ]
)


@router_register.post(
    path="/",
    summary="регистрация пользователя",
    response_model=UserBase
)
async def register_user(
        user: UserCreateModel,
        db: Session = Depends(get_db)
):
    email_new = user.email
    password = user.password
    #    if password != password2:
    #         raise ErrorResponseModel(code=403, message="Ваши пароли не совпадают")
    user_is_in_db = True if await get_user(email=email_new, db=db) else False
    if user_is_in_db:
        raise ErrorResponseModel(code=403, message="Пользователь с такой почтой существует")
    company_name = await write_add_info_user(email=email_new)
    user_c = UserCreate(email=email_new, is_active=False, password=password, company_name_clearbit=company_name)
    user_create = await create_user(db=db, obj_in=user_c)
    return user_create


@router_register.post(
    path="/referal",
    summary="регистрация пользователя по реферальной программе",
    response_model=UserBase
)
async def register_user_referal(
        user: UserCreateReferalModel,
        db: Session = Depends(get_db),
        dict_ref_cod: dict = Depends(check_data_ref_cod)
):
    email_new = user.email
    password = user.password
    user_is_in_db = True if await get_user(email=email_new, db=db) else False
    if user_is_in_db:
        raise ErrorResponseModel(code=403, message="Пользователь с такой почтой существует")
    company_name = await write_add_info_user(email=email_new)
    user_c = UserCreate(email=email_new, is_active=False, password=password, company_name_clearbit=company_name)
    user_create = await create_user(db=db, obj_in=user_c)
    user_referal_id = user_create.id
    await add_in_referal_program(db=db, user_referal_id=user_referal_id, referer_cod=user.referer_cod)
    # return user_create
    return {"message": f"Пользователь зарегистрирован по реферальной программе {dict_ref_cod['referer_email']}"}
