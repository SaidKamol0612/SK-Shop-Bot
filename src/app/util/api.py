import httpx
from typing import Optional


async def get_api_response(url: str, params: Optional[dict] = None) -> dict:
    """
    Make a GET request to the specified URL with optional parameters.

    Args:
        url (str): The URL to send the request to.
        params (dict, optional): A dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the API.

    Raises:
        httpx.HTTPStatusError: For non-2xx HTTP responses.
        httpx.RequestError: For network-related errors.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        raise
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}")
        raise
