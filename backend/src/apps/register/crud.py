from typing import Annotated

from sqlalchemy.orm import Session

from backend.src.apps.register.schemas import ReferalProgramModel
from backend.src.apps.user.crud import get_user_on_referer_cod
from backend.src.apps.user.schemas import UserIsActiveModel, UserCreate, UserSchema
from backend.src.base.crud import CRUDBase
from backend.src.core.security import get_password_hash
from backend.src.models import User, ReferalProgram


async def create_user(
        db: Session,
        *,
        obj_in: UserCreate
) -> User:
    """
    Создание пользвоателя с хэшированным паролем и возвращение его
    :param db: подключение к базе данных
    :param obj_in: входные данные для создания пользователя
    :return: созданного пользователя
    """
    db_obj = User(
        **obj_in.model_dump()
    )
    db_obj.password = await get_password_hash(obj_in.password)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


async def add_in_referal_program(
        db: Session,
        user_referal_id: int,
        referer_cod: str
):
    """
    Добавления реферала по реферальному коду при регистрации
    :param db: сессия бд
    :param user_referal_id: id user, который региструется по реф коду
    :param referer_cod: сам реферальный код
    :return:
    """
    referer_user = await get_user_on_referer_cod(db=db, referer_cod=referer_cod)
    ref_pro_add = ReferalProgramModel(referal_id=user_referal_id, referer_user=referer_user.id)
    ref_pro = CRUDBase(ReferalProgram)
    new_referal = ref_pro.create(db=db, obj_in=ref_pro_add)
    return new_referal
