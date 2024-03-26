import os

import requests
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
    response = await asyncio.to_thread(requests.get, url, headers=headers)
    if response.status_code == 200:
        return response.json()['company']['name']
    return None

