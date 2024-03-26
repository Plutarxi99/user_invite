import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(BASE_DIR / '.env')


# Настройки для приложения
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # секретный ключ для сервиса
    ALGORITHM: str = "HS256"  # алгоритм для создания хэшированного пароля
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # время протухания токена
    COOKIE_NAME: str = os.getenv("COOKIE_NAME")  # названия присваемого токена в cookie

    SUPERUSER_EMAIL: str = os.getenv("SUPERUSER_EMAIL")  # email суперпользователя или первого в бд
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")  # пароль суперпользователя или первого в бд

    EMAIL_TEST_USER: str = os.getenv("EMAIL_TEST_USER")  # email тестового пользователя
    PASSWORD_TEST_USER: str = os.getenv("PASSWORD_TEST_USER")  # пароль тестового пользователя

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_DRIVER: str = os.getenv("POSTGRES_DRIVER")

    # ссылка для подключения к базe данных
    SQLALCHEMY_DATABASE_URI: str = (f"{POSTGRES_DRIVER}://"
                                    f"{POSTGRES_USER}:"
                                    f"{POSTGRES_PASSWORD}@"
                                    f"{POSTGRES_SERVER}/"
                                    f"{POSTGRES_DB}")

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_PORT: str = os.getenv("MAIL_PORT")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")

    CLEARBIT_API_SECRET: str = os.getenv("CLEARBIT_API_SECRET")
    CLEARBIT_API_PUBLIC: str = os.getenv("CLEARBIT_API_PUBLIC")

    REDIS_SERVER: str = os.getenv("REDIS_SERVER")


settings = Settings()
