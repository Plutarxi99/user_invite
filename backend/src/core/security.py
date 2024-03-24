from datetime import timedelta, datetime, timezone

from fastapi.security import OAuth2
from jose import jwt
from passlib.context import CryptContext
from starlette import status


from typing import Optional

from fastapi.exceptions import HTTPException

from starlette.requests import Request

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password, hashed_password):
    """
    Проверка пароля отправленного на сервер
    :param plain_password: вводимый пароль
    :param hashed_password: пароль в базе данных
    :return: если пользователь ввел правильный пароль, то возвращает True, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    """
    Хэширование пароля
    :param password: вводимый пароль при авторизации
    :return: возвращает хэшированный пароль
    """
    return pwd_context.hash(password)


async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Создание токена и возвращение его с установкой времени протухания
    :param data: префикс для опредеения приложения для чего созданного
    :param expires_delta: время протухания
    :return: bearer token
    """
    to_encode = data.copy()
    # установка времени токена
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # создание токена
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Переопределение класса для установки токена и проверка авторизации пользователя
    """

    async def __call__(self, request: Request) -> Optional[str]:
        # установка в cookie пользователю bearer token
        authorization: str = request.cookies.get(settings.COOKIE_NAME)
        # scheme, param = get_authorization_scheme_param(authorization)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return authorization
