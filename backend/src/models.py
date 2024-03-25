from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.src.database import Base


# модели для создания таблице в базе данных
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(45), nullable=True)
    last_name = Column(String(60), nullable=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    referer_cod = Column(String, nullable=True, unique=True)
    referal_user = relationship("ReferalProgram", back_populates="referal")
    company_name_clearbit = Column(String, nullable=True)


class ReferalProgram(Base):
    __tablename__ = 'referal_program'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    referer_user = Column(Integer)

    referal_id = Column(Integer, ForeignKey("users.id"), unique=True)
    referal = relationship("User", back_populates="referal_user")

