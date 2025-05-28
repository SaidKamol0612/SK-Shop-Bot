import httpx

from app.core.config import settings


async def login() -> str:
    url = settings.api.login_endpoint
    data = {"login": settings.api.login, "password": settings.api.password}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data["token"]


async def get_products_from_api(lang: int) -> dict:
    langs = {"uz": 1, "ru": 2}
    url = settings.api.products_endpoint

    bearer_token = await login()
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"languageId": langs.get(lang)}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()