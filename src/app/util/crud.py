def get_categories_by_products(products: list[dict]) -> list[dict]:
    categories = {product['category'] for product in products if 'category' in product}
    return [{'name': category} for category in categories]