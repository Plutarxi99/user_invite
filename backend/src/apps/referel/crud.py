from sqlalchemy.orm import Session
from backend.src.apps.user.schemas import UserInfoReferal
from backend.src.base.crud import write_modeldb_in_modelschema
from backend.src.models import User, ReferalProgram


async def get_referal_on_id(
        db: Session,
        user_referer_id: int
) -> list:
    """
    Получение списка рефералов, которые использовали реферальный код для регистрации
    :param db: получение сессии бд
    :param user_referer_id: id реферера полученного из реферального кода
    :return: список из рефералов подписанного на реферера
    """
    users = db.query(ReferalProgram).filter(ReferalProgram.referer_user == user_referer_id).all()
    users_list = []
    for u in users:
        user_referal = await write_modeldb_in_modelschema(u.referal, UserInfoReferal)
        users_list.append(user_referal)
    return users_list
