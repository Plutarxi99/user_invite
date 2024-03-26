from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.src.apps.auth.schemas import LoginModel, TokenAcceptEmail
from backend.src.apps.user.crud import get_user_on_id
from backend.src.apps.user.schemas import UserIsActiveModel
from backend.src.base.crud import CRUDBase
from backend.src.core.config import settings
from backend.src.core.security import create_access_token
from backend.src.exceptions.model import ErrorResponseModel
from backend.src.services.mail_server.mail_conf import send_mail
from backend.src.services.mail_server.schema import EmailBody
from backend.src.models import User
from backend.src.operations.deps import authenticate_user, get_db

router_auth = APIRouter(

)


@router_auth.post(
    "/login",
    summary="Вход в систему",

    # response_model=UserInfo,
    # response_model_exclude_none=True
)
async def login_user(
        response: Response,
        user: LoginModel,
        db: Session = Depends(get_db),
):
    """
    Эндпоинт для входа существующего пользователя
    :param response: для установки токена для использования сервиса
    :param user: схема для входa пользователя
    :param db: получение подключения к сессии базе данных
    :return: возвращает существующего пользователя
    """
    # для получения существующего пользователя
    user_in = await authenticate_user(
        email=user.login,
        password=user.password,
        db=db
    )
    # проверка есть ли пользователь
    if not user_in:
        raise ErrorResponseModel(
            code=401,
            message="Такого пользователя не существует в системе"
        )
    # установка времени протухания токена, создание и присваивания токена
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = await create_access_token(
        data={"sub": user.login},
        expires_delta=access_token_expires
    )
    # отправка письма с bearer token и делаем объект для вложения в функцию
    send_obj_mail = EmailBody(pk=user_in.id,
                              to=user_in.email,
                              subject="токен для использование системы",
                              message=TokenAcceptEmail(
                                  access_token=access_token,
                                  token_type=settings.COOKIE_NAME,
                                  pk=user_in.id
                              ).model_dump_json()
                              )

    status_send_mail = await send_mail(send_obj_mail)
    # Если без отправки письма, то раскоммитить след строки
    # а другой return закоммитить
    #     plug_without_send_mail = {
    #         "access_token": access_token,
    #         "token_type": "bearer",
    #         "pk": user_in.id}
    #     return {"answer": plug_without_send_mail}
    if status_send_mail:
        return {"answer": "Письмо отправлено на почту для вхождения в систему"}
    else:
        return {"answer":"Письмо не отправлено или произошла ошибка на сервере"}


@router_auth.post(
    "/set_cookie_bearer",
    summary="Установка bearer токена для использования системы",
)
async def accept_email_register(
        response: Response,
        bearer_token: TokenAcceptEmail,
        db: Session = Depends(get_db)
):
    """
    Установка на браузер пользователя
    Cookie bearer token для использования сервисом
    :param response:
    :param bearer_token:
    :param db:
    :return:
    """
    current_user_not_active = await get_user_on_id(user_id=bearer_token.pk, db=db)
    user_is_active = UserIsActiveModel(
        email=current_user_not_active.email,
        is_active=True
    )
    # обновление в базе данных, что пользователь активен
    user = CRUDBase(model=User)
    user.update(db=db, obj_in=user_is_active, db_obj=current_user_not_active)
    # установка в cookie bearer token
    response.set_cookie(key=bearer_token.token_type,
                        value=f"{bearer_token.access_token}"
                        )

    return {"message": "Установлен токен для использования сервисом"}


@router_auth.get(
    "/logout",
    summary="Выход из системы"
)
async def logout_user(
        response: Response
):
    """
    Эндпоинт для удаления bearer token из cookie в браузере пользователя
    :param response: для удаления bearer token из cookie в браузере пользователя
    :return:
    """
    # удаление токена
    response.delete_cookie(key=settings.COOKIE_NAME)
    return {"Выход": "Вы уже вышли из системы"}
