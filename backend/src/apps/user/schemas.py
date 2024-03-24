from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr | None = "plutarx@grek.ru"

    class Config:
        orm_mode = True
        from_attributes = True


class UserCreate(UserBase):
    password: str
    is_active: bool | None = False
    company_name_clearbit: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True


class UserIsActiveModel(UserBase):
    is_active: bool

    class Config:
        orm_mode = True
        from_attributes = True


class UserInfoReferal(UserBase):
    first_name: str | None = "Plutarx"
    last_name: str | None = "Luckreci"


class UserInfoReferalDoc(BaseModel):
    email_referer: EmailStr | None = "plutarx@grek.ru"
    referals: list[UserInfoReferal] | None = None


class UserInfo(UserInfoReferal):
    referer_cod: str
    is_admin: bool | None = False
    is_active: bool | None = True

    class Config:
        orm_mode = True
        from_attributes = True


class UserSchema(UserInfo):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: str | None = "Plutarx"
    last_name: str | None = "Luckreci"

    class Config:
        orm_mode = True
        from_attributes = True