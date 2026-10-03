import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get('/inventory')

    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_item(client):
    response = client.get('/inventory/1')

    assert response.status_code == 200
    assert response.json["id"] == 1

def test_get_item_not_found(client):
    response = client.get('/inventory/999')

    assert response.status_code == 404
    assert response.json["error"] == "Item not found"

def test_add_item(client):
    new_item = {
        "name": "Test Item",
        "category": "Test Category",
        "price": 100,
        "stock": 10
    }

    response = client.post('/inventory', json=new_item)

    assert response.status_code == 201
    assert response.json["name"] == new_item["name"]

def test_update_item(client):
    response = client.patch('/inventory/1', json={
        "price": 250,
        "stock": 50 
        })
    
    assert response.status_code == 200
    assert response.json["price"] == 250
    assert response.json["stock"] == 50

def test_delete_item(client):
    response = client.delete('/inventory/1')

    assert response.status_code == 200
    assert response.json["message"] == "Item deleted successfully"
