from sqlalchemy.orm import Session

from backend.src.models import User


async def get_user(
        email: str,
        db: Session
) -> User:
    """
    Получение пользователя по email из базы данных
    :param email: email пользователя
    :param db: подключение к базе данных
    :return: пользователя из базы данных
    """
    user = db.query(User).filter(User.email == email).first()
    return user


async def get_user_on_id(
        user_id: int,
        db: Session
):
    """
    Получение пользователя из базы данных по id в базе данных
    :param user_id:  id пользователя
    :param db: подключении к базе данных
    :return: пользователя из базы данных
    """
    user = db.query(User).filter(User.id == user_id).first()
    return user


async def get_user_on_referer_cod(
        referer_cod: str,
        db: Session
):
    """
    Получение пользователя из базы данных по referer_cod в базе данных
    :param referer_cod:  referer_cod пользователя
    :param db: подключении к базе данных
    :return: пользователя из базы данных
    """
    user = db.query(User).filter(User.referer_cod == referer_cod).first()
    return user
