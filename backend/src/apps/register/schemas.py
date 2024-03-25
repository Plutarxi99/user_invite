from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    email: EmailStr
    password: str


class UserCreateReferalModel(UserCreateModel):
    referer_cod: str | None = None


class ReferalProgramModel(BaseModel):
    referer_user: int
    referal_id: int
