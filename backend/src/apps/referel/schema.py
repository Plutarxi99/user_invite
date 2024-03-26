from datetime import datetime
from pydantic import BaseModel, EmailStr


class MyRefCod(BaseModel):
    final_data: datetime = None


class RefCodSearch(BaseModel):
    referer_email: EmailStr
    final_data: datetime = None


class RefererCod(BaseModel):
    referer_cod: str | None = None
