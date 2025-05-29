import json
from pathlib import Path
from datetime import datetime, timedelta
from .api import get_products_from_api

PARENT_DIR = Path(__file__).parent
CACHE_PATH = PARENT_DIR / "cache.json"


def is_stale_json(file_path: Path = CACHE_PATH, max_hours: int = 24) -> bool:
    if not file_path.exists():
        return True

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_at_str = data.get("updated_at")
    if not updated_at_str:
        return True

    try:
        updated_at = datetime.fromisoformat(updated_at_str)
    except ValueError:
        return True

    return datetime.now() - updated_at > timedelta(hours=max_hours)


async def get_data(lang: str = None, data_type: str = "categories") -> dict:
    if is_stale_json():
        data = await get_products_from_api(lang)
        updated_at = datetime.now().isoformat()

        categories = [product["category"] for product in data]

        new_data = {
            "updated_at": updated_at,
            "data": {
                "categories": list(set(categories)),
                "products": data
            },
        }

        with open(CACHE_PATH, "w") as f:
            json.dump(new_data, f)
    else:
        with open(CACHE_PATH, "r") as f:
            new_data = json.load(f)
    return new_data.get("data").get(data_type)
