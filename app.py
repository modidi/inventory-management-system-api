from flask import Flask, jsonify,request
from data.inventory import inventory

app = Flask(__name__)

#Helper function to find an item by ID
def find_item(item_id):
    for item in inventory:
        if item['id'] == item_id:
            return item
    return None

#Routes

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
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

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json() or {}

    allowed_fields = ["name", "category", "price", "stock"]

    for field in allowed_fields:
        if field in data:
            item[field] = data[field]  
 
    return jsonify(item), 200


if __name__ == '__main__':
    app.run(debug=True)