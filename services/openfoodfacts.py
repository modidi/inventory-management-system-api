import requests

def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"

    headers = {
        "User-Agent": "InventoryMangementSystem/1.0"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    product_data = data.get("product", {})

    return {
        "barcode": barcode,
        "name": product_data.get("product_name", ""),
        "brand": product_data.get("brands", ""),
        "category": product_data.get("categories", ""),
        "quantity": product_data.get("quantity", "")
    }


    return response.json()