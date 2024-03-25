from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from backend.src.apps.auth.schemas import TokenData
from backend.src.apps.referel.schema import MyRefCod, RefCodSearch
from backend.src.apps.user.crud import get_user
from backend.src.apps.user.schemas import UserSchema
from backend.src.core.config import settings
from backend.src.core.security import verify_password, OAuth2PasswordBearerWithCookie
from backend.src.exceptions.model import ErrorResponseModel
from backend.src.models import User
import base64
import pickle
import pytz
oauth2_scheme = OAuth2PasswordBearerWithCookie()


async def get_db(request: Request):
    """
    Получение подключение к базе данных
    :return: сессия подкючение к базе данных
    """
    return request.state.db


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Функция для чтения полученного токена и возвращение ошибки
    :param token: bearer token пользователя
    :param db: подключение к базе данных
    :return: возвращает пользователя
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# async def get_current_user_by_bearer(
#         current_user: Annotated[UserSchema, Depends(get_current_user)]
# ):
#     """
#     Проверка пользователя является ли он админом сервиса
#     :param current_user: пользователь, который делает запрос
#     :return: пользователя, иначе ошибка
#     """
#     if not current_user:
#         raise ErrorResponseModel(code=403, message="Вы не являетесь пользователем сервиса")
#     return current_user


async def get_current_admin_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    """
    Проверка пользователя является ли он админом сервиса
    :param current_user: пользователь, который делает запрос
    :return: пользователя, иначе ошибка
    """
    if not current_user.is_admin:
        raise ErrorResponseModel(code=403, message="Вы не являетесь админом сервиса")
    return current_user


async def authenticate_user(db: Session, email: str, password: str):
    """
    Проверка вхождения пользователя. Проверка пароля и сущетсвет ли такой пользователя
    :param db: подключение к базе данных
    :param email: email вводимым пользователем
    :param password: пароль вводимым пользователем
    :return: возвращает пользователя
    """
    user = await get_user(db=db, email=email)
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


async def create_referer_cod(

):
    """
    Создание уникального реферального кода
    :return: строку из цифр реферального кода
    """
    time_now = datetime.now()
    time_start = datetime(1970, 1, 1)
    diff_time = time_now - time_start
    referal_cod = int(diff_time.total_seconds())
    return str(referal_cod)


async def encode_referer_cod(
        dict_ref_cod: dict
) -> str:
    """
    Кодирование словаря в реферальный код
    :param dict_ref_cod: словарь с данными
    :return: реферальный код реферера
    """
    referer_cod = base64.b64encode(pickle.dumps(dict_ref_cod)).decode()
    # dict_decoded = pickle.loads(base64.b64decode(encoded_string))
    return referer_cod


async def decode_referer_cod(
        request: Request
) -> dict:
    dict_encode_ref_cod = await request.json()
    encode_ref_cod = dict_encode_ref_cod['referer_cod']
    if encode_ref_cod == 'null':
        raise ErrorResponseModel(code=403, message="Реферальный код не верный или такого не существует")
    decode_ref_cod = pickle.loads(base64.b64decode(encode_ref_cod))
    return decode_ref_cod


async def check_data_ref_cod(
        # dict_ref_cod: Annotated[RefCodSearch, Depends(decode_referer_cod)]
        dict_ref_cod: Annotated[RefCodSearch, Depends(decode_referer_cod)]
):
    # date = dict_ref_cod.final_data
    utc = pytz.UTC
    date = dict_ref_cod['final_data']
    now_data = utc.localize(datetime.now())
    if now_data > date:
        raise ErrorResponseModel(code=403, message="Реферальный код истек")
    return dict_ref_cod


def create_user_schema(user: User):
    schema = UserSchema(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        referer_cod=user.referer_cod,
        is_admin=user.is_admin,
        is_active=user.is_active
    )
    return schema
