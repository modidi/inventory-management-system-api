from flask import Flask, jsonify,request, session
from data.inventory import inventory
from services.openfoodfacts import get_product_by_barcode, search_products_by_name

app = Flask(__name__)
app.secret_key = "inventory-secret-key"

#Helper functions

#Get logged-in user
def current_username():
    return session.get("username")

#Check Login
def login_required():
    if not current_username():
        return jsonify({"error": "Login required"}), 401
    return None

#Find item by ID
def find_item(item_id):
    for item in inventory:
        if item['id'] == item_id:
            return item
    return None

#Admin Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if username != "admin" or password != "admin123":
        return jsonify({"error":"Invalid username or password"}), 401

    session["username"] = username

    return jsonify({"message": "Login successful"}), 200

#Admin logout
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)

    return jsonify({"message": "Logged out successfully"}), 200

#Routes

#Get all inventory items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    error = login_required()
    if error:
        return error

    return jsonify(inventory), 200

#Get one inventory item by ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    error = login_required()
    if error:
        return error

    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200

#Add a new inventory item
@app.route("/inventory", methods=["POST"])
def add_item():
    error = login_required()
    if error:
        return error

    data = request.get_json()
    
    new_item = {
        "id": max([item["id"] for item in inventory], default=0) + 1,
        "name": data["name"],
        "category": data["category"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)
    return jsonify(new_item), 201

#Update an inventory item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    error = login_required()
    if error:
        return error

    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json() or {}

    allowed_fields = ["name", "category", "price", "stock"]

    for field in allowed_fields:
        if field in data:
            item[field] = data[field]  
 
    return jsonify(item), 200

#Delete an inventory item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    error = login_required()
    if error:
        return error

    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Item deleted successfully"}), 200

#Barcode search
@app.route("/product/barcode/<barcode>", methods=["GET"])
def get_product(barcode):
    product = get_product_by_barcode(barcode)
    return jsonify(product), 200

#Name search
@app.route("/product/name/<name>", methods=["GET"])
def search_product(name):
    products = search_products_by_name(name)
    return jsonify(products), 200

#Add API product to inventory
@app.route("/inventory/from-product/<barcode>", methods=["POST"])
def add_product_from_api(barcode):
    error = login_required()
    if error:
        return error
        
    product = get_product_by_barcode(barcode)

    if not product or not product.get("name"):
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json() or {}

    new_item = {
        "id": max([item["id"] for item in inventory], default=0) + 1,
        "barcode": product["barcode"],
        "name": product["name"],
        "brand": product["brand"],
        "category": product["category"],
        "quantity": product["quantity"],
        "price": data.get("price",0), 
        "stock": data.get("stock",0)   
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == '__main__':
    app.run(debug=True)