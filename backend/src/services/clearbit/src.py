import os

import requests
from backend.src.core.config import settings
import asyncio

secret_key = os.getenv("CLEARBIT_API_SECRET")


async def write_add_info_user(email: str):
    """
    Вызов эндпоинта API clearbit на получение доп информации
    :param email: email клиента
    :return: название компании
    """
    url = f"https://person-stream.clearbit.com/v2/combined/find?email={email}"

    headers = {"Authorization": f"Bearer {secret_key}"}
    # response = requests.get(url, headers=headers)
    response = await asyncio.to_thread(requests.get, url, headers=headers)
    if response.status_code == 200:
        return response.json()['company']['name']
    return None

    # company_name = asyncio.run(write_add_info_user(email=email)


# async def get_company_name(email: str):
#     company_name = asyncio.run(write_add_info_user(email="shievanov@bk.ru"))
#     return company_name
# a = asyncio.run(write_add_info_user(email="qwe123@gmail.com"))
# print(a)
