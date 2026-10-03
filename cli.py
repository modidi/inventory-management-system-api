import requests

BASE_URL = "http://127.0.0.1:5000"

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        for item in items:
            print(item)
    else:
        print("Error:", response.status_code)

def view_item(item_id):
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        item = response.json()
        print(item)
    else:
        print("Error:", response.status_code)

def add_item():
    name = input("Enter item name: ")
    category = input("Enter item category: ")
    price = get_float("Enter item price: ")
    stock = get_int("Enter item stock: ")

    data = {
        "name": name,
        "category": category,
        "price": price,
        "stock": stock
    }

    response = requests.post(f"{BASE_URL}/inventory", json=data)

    if response.status_code == 201:
        item = response.json()
        print("Item added:", item)  
    else:
        print("Error:", response.status_code)

def update_item(item_id):
    price = input("Enter new price (leave blank to keep current): ")
    stock = input("Enter new stock (leave blank to keep current): ")

    data = {}

    if price:
        try:
            data["price"] = float(price)
        except ValueError:
            print("Invalid price. Please enter a number.")
            return

    if stock:
        try:
            data["stock"] = int(stock)
        except ValueError:
            print("Invalid stock. Please enter a whole number.")
            return

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)

    if response.status_code == 200:
        item = response.json()
        print("Item updated:", item)  
    else:
        print("Error:", response.status_code)

def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        print("Item deleted successfully.")
    else:
        print("Error:", response.status_code)

def find_product_by_barcode(barcode):
    response = requests.get(f"{BASE_URL}/product/barcode/{barcode}")

    if response.status_code == 200:
        product = response.json()
        print(product)
    else:
        print("Error:", response.status_code)

def find_products_by_name(name):
    response = requests.get(f"{BASE_URL}/product/name/{name}")

    if response.status_code == 200:
        products = response.json()

        for product in products:
            print(product)
    else:
        print("Error:", response.status_code)

def add_product_from_api():
    barcode = input("Enter product barcode: ")
    price = get_float("Enter item price: ")
    stock = get_int("Enter item stock: ")
    
    data = {
        "price": price,
        "stock": stock  
    }

    response = requests.post(f"{BASE_URL}/inventory/from-product/{barcode}", json=data)

    if response.status_code == 201:
        item = response.json()
        print("Product added to inventory:")
        print(item)  
    else:
        print("Error:", response.status_code)
    
def menu():
    while True:
        print("\n===== Inventory Management System =====") 
        print("1. View all Inventory")
        print("2. View one item")
        print("3. Add Item")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Find Product by Barcode")
        print("7. Find Product by Name")
        print("8. Add Product from OpenFoodFacts API")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            item_id = get_int("Enter item ID to view: ")
            view_item(item_id)

        elif choice == "3":
            add_item()

        elif choice == "4":
            item_id = get_int("Enter item ID to update: ")
            update_item(item_id)

        elif choice == "5":
            item_id = get_int("Enter item ID to delete: ")
            delete_item(item_id)

        elif choice == "6":
            barcode = input("Enter product barcode: ")
            find_product_by_barcode(barcode)

        elif choice == "7":
            name = input("Enter product name: ")
            find_products_by_name(name)

        elif choice == "8":
            add_product_from_api()

        elif choice == "9":
            print("Exiting the program.")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()