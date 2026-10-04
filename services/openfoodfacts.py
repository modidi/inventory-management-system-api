import requests

def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching product data for barcode {barcode}: {e}")
        return None

    product_data = data.get("product")

    if not product_data or not product_data.get("product_name"):
        return None

    return {
        "barcode": barcode,
        "name": product_data.get("product_name", ""),
        "brand": product_data.get("brands", ""),
        "category": product_data.get("categories", ""),
        "quantity": product_data.get("quantity", "")
    }

def search_products_by_name(name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5
    }

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error searching for product {name}: {e}")
        return []

    products = data.get("products", [])

    return [
        {
            "barcode": product.get("_id", ""),
            "name": product.get("product_name", ""),
            "brand": product.get("brands", ""),
            "category": product.get("categories", ""),
            "quantity": product.get("quantity", "")
        }
        for product in products 
    ]