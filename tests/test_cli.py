from unittest.mock import patch, Mock

import cli

@patch("cli.client.get")
def test_view_inventory(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1, 
            "name": "Vanilla Yoghurt", 
            "category": "Dairy", 
            "price": 10.0, 
            "stock": 20
        }
    ]

    mock_get.return_value = mock_response

    cli.view_inventory()

    captured = capsys.readouterr()
    assert "Vanilla Yoghurt" in captured.out

@patch("cli.client.post")
def test_add_item(mock_post, monkeypatch, capsys):
    inputs = iter([
        "Test Product",
        "Test Category",
        "10.0",
        "100"
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 5,
        "name": "Test Product",
        "category": "Test Category",
        "price": 10.0,
        "stock": 100
    }

    mock_post.return_value = mock_response

    cli.add_item()

    captured = capsys.readouterr()

    assert "Test Product" in captured.out

@patch("cli.client.patch")
def test_update_item(mock_patch, monkeypatch, capsys):
    inputs = iter([
        "20.0",
        "200"
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Vanilla Yoghurt",
        "price": 20.0,
        "stock": 200
    }

    mock_patch.return_value = mock_response

    cli.update_item(1)

    captured = capsys.readouterr()

    assert "Item updated" in captured.out
    mock_patch.assert_called_once_with(
        "http://127.0.0.1:5000/inventory/1",
        json={"price": 20.0, "stock": 200}  
    )
@patch("cli.client.delete")
def test_delete_item(mock_delete, capsys):
    mock_response = Mock()
    mock_response.status_code = 200

    mock_delete.return_value = mock_response

    cli.delete_item(1)

    captured = capsys.readouterr()

    assert "Item deleted successfully" in captured.out

    mock_delete.assert_called_once_with("http://127.0.0.1:5000/inventory/1")


  