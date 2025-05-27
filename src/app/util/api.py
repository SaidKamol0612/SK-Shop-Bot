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

async def send_order_to_api(user_name: str, user_number: str, products: list[dict]) -> dict:
    
    url = settings.api.send_order_endpoint

    bearer_token = await login()
    headers = {"Authorization": f"Bearer {bearer_token}"}
    data = {
        "customerData": {
            "name": user_name,
            "phoneNumber": user_number
        },
        "products": [],
        "totalAmount": 0
    }
    total_amount = 0
    for product in products:
        data["products"].append({
            "productId": product["id"],
            "count": product["count"]
        })
        total_amount += product["count"]
        
    data["totalAmount"] = total_amount
    print(f"Sending order data: {data}")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()