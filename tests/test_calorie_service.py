from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app  # Ensure app is correctly imported

client = TestClient(app)

# Mocked USDA API response for valid dish
def mock_usda_api_valid_dish(*args, **kwargs):
    # Create a mock response object
    mock_response = MagicMock()
    mock_response.status_code = 200  # Simulate a successful response
    mock_response.json.return_value = {"foods": [
        {"foodNutrients": [{"nutrientName": "Energy", "value": 150, "unitName": "kcal"}]}
    ]}
    return mock_response

# Test: Create user, log in, and then make a request with the Bearer token
@patch('app.services.dish.requests.get', side_effect=mock_usda_api_valid_dish)
def test_create_user_and_get_calories(mock_get):
    # Step 1: Try to log in first
    login_data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }

    response = client.post("/auth/login", json=login_data)
    
    if response.status_code == 401:  # If login fails (user not found)
        # Step 2: Register the user if login fails
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200
        assert response.json()["msg"] == "User created successfully"
    
        # Step 3: Log in again after registering
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        print("Login Response:", response.json())  # Debugging: print the login response

    # Extract the Bearer token
    token = response.json().get("access_token", None)
    print("My Token:", token)
    
    # Step 4: Use the Bearer token to make a request to /get-calories
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/get-calories", json={"dish_name": "Apple", "servings": 2}, headers=headers)
    assert response.status_code == 200
    assert response.json()["total_calories"] == 300  # Assuming 150 kcal per serving * 2 servings
