from pydantic import EmailStr, BaseModel


class EmailBody(BaseModel):
    pk: int
    to: EmailStr
    subject: str
    message: str
