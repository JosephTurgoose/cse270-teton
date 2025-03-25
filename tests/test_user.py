import requests
import pytest
from pytest_mock import mocker

def mock_requests_get(url, params=None, **kwargs):
    if params == {"username": "admin", "password": "admin"}:
        return MockResponse("", 401)
    elif params == {"username": "admin", "password": "qwerty"}:
        return MockResponse("", 200)
    return MockResponse("Not Found", 404)

class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

@pytest.mark.parametrize("params, expected_status", [
    ({"username": "admin", "password": "admin"}, 401),
    ({"username": "admin", "password": "qwerty"}, 200)
])
def test_admin_authentication(mocker, params, expected_status):
    url = "http://127.0.0.1:5500/teton/1.6/admin.html"
    mocker.patch("requests.get", side_effect=mock_requests_get)
    
    response = requests.get(url, params=params)
    
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    assert response.text == "", f"Expected empty response, got: {response.text}"
