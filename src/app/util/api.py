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
    test_products = [
        {
            "id": 1,
            "name": "Test Product",
            "price": 100.0,
            "category": "Example Category 1",
            "shortDescription": "This is a test product.",
            "images": [{"filePath": "https://picsum.photos/200/300"}]
        },
        {
            "id": 2,
            "name": "Another Test Product",
            "price": 150.0,
            "category": "Example Category 2",
            "shortDescription": "This is another test product.",
            "images": [{"filePath": "https://picsum.photos/200/300"}]
        },
        {
            "id": 3,
            "name": "Sample Product",
            "price": 200.0,
            "category": "Example Category 3",
            "shortDescription": "This is a sample product.",
            "images": [{"filePath": "https://picsum.photos/200/300"}]
        },
        {
            "id": 4,
            "name": "Demo Product",
            "price": 250.0,
            "category": "Example Category 4",
            "shortDescription": "This is a demo product.",
            "images": [{"filePath": "https://picsum.photos/200/300"}]
        },
        {
            "id": 5,
            "name": "Example Product",
            "price": 300.0,
            "category": "Example Category 5",
            "shortDescription": "This is an example product.",
            "images": [{"filePath": "https://picsum.photos/200/300"}]
        },
        {
            "id": 6,
            "name": "Test Product 2",
            "price": 120.0,
            "category": "Example Category 6",
            "shortDescription": "This is a second test product.",
            "images": [{"filePath": "https://picsum.photos/200/300"}]
        }
    ]
    return test_products
    
    langs = {"uz": 1, "ru": 2}
    url = settings.api.products_endpoint

    bearer_token = await login()
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"languageId": langs.get(lang)}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
