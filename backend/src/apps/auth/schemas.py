from pydantic import BaseModel, EmailStr


# схемы для ответов и получения данных
class LoginModel(BaseModel):
    login: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenAcceptEmail(Token):
    pk: int


class TokenData(BaseModel):
    email: str | None = None
