import requests
from unittest.mock import patch, Mock
from services.openfoodfacts import get_product_by_barcode

@patch('services.openfoodfacts.requests.get')
def test_get_product_by_barcode(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "product": {
            "product_name": "Test Chocolate",
            "brands": "Test Brand",
            "categories": "Chocolate",
            "quantity": "100 g"
        }
    }
    
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_product_by_barcode("123456789")

    assert result["barcode"] == "123456789"
    assert result["name"] == "Test Chocolate"
    assert result["brand"] == "Test Brand"
    assert result["category"] == "Chocolate"
    assert result["quantity"] == "100 g"

@patch("services.openfoodfacts.requests.get")
def test_get_product_by_barcode_api_failure(mock_get):
    mock_get.side_effect = requests.RequestException("API failure")

    result = get_product_by_barcode("123456789")

    assert result is None