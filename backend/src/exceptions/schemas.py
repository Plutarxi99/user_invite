from pydantic import BaseModel


# схемы для ответов и получения данных
class ErrorResponseSchema(BaseModel):
    code: int
    message: str
