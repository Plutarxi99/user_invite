import os
from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy.orm import Session

from backend.src.apps.referel.crud import get_referal_on_id
from backend.src.apps.referel.schema import (MyRefCod,
                                             RefCodSearch,
                                             RefererCod)
from backend.src.apps.user.crud import get_user, get_user_on_id
from backend.src.apps.user.schemas import (UserSchema,
                                           UserBase,
                                           UserInfoReferalDoc)
from backend.src.base.crud import CRUDBase
from backend.src.exceptions.model import ErrorResponseModel
from backend.src.models import User
from backend.src.operations.deps import (get_current_active_user,
                                         get_db,
                                         encode_referer_cod)
import aioredis

router_referal = APIRouter(
    dependencies=[
        Depends(get_current_active_user)
    ]
)


@router_referal.get(
    "/current_ref_cod",
    summary="Получение действующего реферального кода",
    response_model=RefererCod
)
async def get_my_current_ref_cod(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    key_redis = str(current_user.id) + "_ref"
    value_redis = current_user.referer_cod
    if value_redis is None:
        raise ErrorResponseModel(
            code=404,
            message="У вас нет реферального кода"
        )
    redis = await aioredis.from_url(os.getenv("REDIS_SERVER"))
    get_refcod_in_redis = await redis.get(key_redis)
    if get_refcod_in_redis:
        return RefererCod(
            referer_cod=get_refcod_in_redis
        ).model_dump()
    else:
        await redis.set(key_redis, value_redis, ex=3600)
        await redis.close()
        await redis.wait_closed()
        return current_user


@router_referal.post(
    "/my_cod",
    summary="получи свой реферальный код",
    response_model=RefererCod
)
async def get_my_referal_cod(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
        finaldata: MyRefCod,
        db: Session = Depends(get_db)
):
    """
    Получение авторизованным пользовтелем своего реферарального кода
    :param current_user: авторизованный пользователь
    :param finaldata: дата протухания реферального кода
    :param db: подключение к базе данных
    :return: реферальный код
    """
    email = current_user.email
    user_in_db = await get_user(email=email, db=db)
    # заполняем нужную модель для записи реферального кода
    dict_ref_cod = RefCodSearch(referer_email=email, **finaldata.model_dump()).model_dump()
    enc_ref_cod = await encode_referer_cod(dict_ref_cod)
    # записываем в схему-модель и записываем в
    # базу данных реферальный код пользователя
    ref_cod = RefererCod(referer_cod=enc_ref_cod)
    user = CRUDBase(model=User)
    user_ref_cod = user.update(db=db, obj_in=ref_cod, db_obj=user_in_db)
    return user_ref_cod


@router_referal.get(
    "/d_my_ref_cod",
    summary="Удаление своего реферального кода",
    response_model=RefererCod
)
async def delete_my_ref_cod(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
):
    user_db = await get_user(email=current_user.email, db=db)
    if not current_user.referer_cod:
        raise ErrorResponseModel(
            code=401,
            message="У вас уже удален реферальный код"
        )
    ref_cod = RefererCod(referer_cod=None)
    user = CRUDBase(model=User)
    user_not_ref_cod = user.update(
        db=db,
        obj_in=ref_cod,
        db_obj=user_db
    )
    return user_not_ref_cod


@router_referal.get(
    "/get_my_referals",
    summary="получи список рефералов подписанных на тебя",
    response_model=UserInfoReferalDoc

)
async def get_list_my_referals(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Получение списка рефералов аунтифированным пользователем:
    :param current_user: проверка и получени .что пользователь аунтифирован
    :param db: полчение сесии подключеник к дб
    :return: список твоих рефералов
    """
    email = current_user.email
    user_referer = await get_user(email=email, db=db)
    user_referer_id = user_referer.id
    list_referals = await get_referal_on_id(
        db=db,
        user_referer_id=user_referer_id
    )
    l_r = UserInfoReferalDoc(
        email_referer=user_referer.email,
        referals=list_referals
    )
    return l_r


@router_referal.post(
    "/get_refcod_on_email",
    response_model=RefererCod,
    summary="получение реферального кода по email"

)
async def get_referer_cod_on_email(
        referer_email: UserBase,
        db: Session = Depends(get_db)
):
    referer = await get_user(email=referer_email.email, db=db)
    if not referer:
        raise ErrorResponseModel(
            code=403,
            message="Пользователь с такой почтой не существует"
        )
    ref_cod = referer.referer_cod
    if not ref_cod:
        raise ErrorResponseModel(
            code=403,
            message="Пользователь с такой почтой не имеет реферального кода"
        )
    return RefererCod(referer_cod=ref_cod)


@router_referal.get(
    "/get_referals/{id_referer}",
    summary="получение информации о рефералах id реферера",
    response_model=UserInfoReferalDoc
)
async def get_referals_in_id_referer(
        id_referer: int,
        db: Session = Depends(get_db)
):
    referer = await get_user_on_id(user_id=id_referer, db=db)
    if not referer:
        raise ErrorResponseModel(code=403, message="Пользователь с таким id не существует")
    list_referals = await get_referal_on_id(db=db, user_referer_id=id_referer)
    l_r = UserInfoReferalDoc(
        email_referer=referer.email,
        referals=list_referals
    )
    return l_r
