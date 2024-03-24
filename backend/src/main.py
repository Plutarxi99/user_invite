import pathlib

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination
from starlette.responses import JSONResponse
import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from backend.src.operations.router import api_router
from backend.src.database import engine, SessionLocal
from fastapi import Request, Response
from backend.src.database import Base

from backend.src.exceptions.model import ErrorResponseModel
from backend.src.exceptions.schemas import ErrorResponseSchema
from alembic.config import Config
from alembic import command

from backend.src.core.config import settings

# from backend.src.mail_server import schema
# from starlette.responses import JSONResponse
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)
# строим путь до alembic.ini
file_alembic = pathlib.Path(__file__).parent.parent.joinpath("alembic.ini")
# создаем файл конфигураций, который будет импортирован в alembic.ini
alembic_cfg = Config(file_alembic)
# устанавливаем нахождения миграции в alembic.ini
alembic_cfg.set_main_option("script_location", "backend/migrations")
# устанавливаем ссылку на подключении к базе данных
alembic_cfg.set_main_option("sqlalchemy.url", f"{settings.SQLALCHEMY_DATABASE_URI}")
# автоматическая установка новой миграций
command.upgrade(alembic_cfg, "head")
app = FastAPI()
app.include_router(api_router)
add_pagination(app)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Возвращает подключение к базе данных, пока используется, иначе закрывает подключение
    """
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.exception_handler(ErrorResponseModel)
async def bad_request_400(request: Request, exc: ErrorResponseModel):
    """
    Отлов ошибок и отправка в виде json пользователю
    """
    return JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder(ErrorResponseSchema(code=exc.code, message=exc.message)),
    )

#
#
#
# @app.post("/email")
# async def send_email(body: EmailBody):
#     try:
#         msg = MIMEText(body.message, "html")
#         msg['Subject'] = body.subject
#         msg['From'] = f'Denolyrics <{OWN_EMAIL}>'
#         msg['To'] = body.to
#
#         port = MAIL_PORT  # For SSL
#
#         # Connect to the email server
#         server = SMTP_SSL(MAIL_SERVER, port)
#         server.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)
#
#         # Send the email
#         server.send_message(msg)
#         server.quit()
#         return True
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=e)
# @app.post("/email")
# async def simple_send(email: schema.EmailSchema):
#     html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """
#
#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=email.dict().get("email"),
#         body=html,
#         subtype=MessageType.html)
#
#     fm = FastMail(schema.conf)
#     await fm.send_message(message)
#     return "good"
