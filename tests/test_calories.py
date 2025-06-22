import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport

# Ensure import of app works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

transport = ASGITransport(app=app)

# --- ✅ Shared USDA Mock ---
def mock_usda_api_valid_dish(*args, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "foods": [
            {
                "description": "Apple",
                "foodNutrients": [{"nutrientName": "Energy", "value": 150, "unitName": "kcal"}],
                "servingSize": 100,
            }
        ]
    }
    return mock_response

# --- ✅ Auth Helper ---
async def get_auth_token(client: AsyncClient) -> str:
    login_data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }

    response = await client.post("/auth/login", json=login_data)
    if response.status_code == 401:
        await client.post("/auth/register", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123"
        })
        response = await client.post("/auth/login", json=login_data)

    token = response.json().get("access_token")
    assert token is not None
    return token

# --- ✅ Test: Happy Path ---
@pytest.mark.asyncio
@patch('app.services.dish.requests.get', side_effect=mock_usda_api_valid_dish)
async def test_create_user_and_get_calories(mock_get):
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await get_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        cal_res = await client.post("/get-calories", json={
            "dish_name": "Apple",
            "servings": 2
        }, headers=headers)

        assert cal_res.status_code == 200
        result = cal_res.json()
        assert result["total_calories"] == 300
        assert result["dish_name"] == "Apple"
        assert result["servings"] == 2
        assert result["calories_per_serving"] == 150

# --- ❌ Non-existent Dish ---
@pytest.mark.asyncio
@patch('app.services.dish.requests.get')
async def test_get_calories_dish_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"foods": []}
    mock_get.return_value = mock_response

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await get_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post("/get-calories", json={
            "dish_name": "thisdoesnotexist123",
            "servings": 1
        }, headers=headers)

        assert response.status_code == 404
        assert "Dish not found" in response.text

# --- ⚠️ Zero or Negative Servings ---
@pytest.mark.asyncio
@patch('app.services.dish.requests.get', side_effect=mock_usda_api_valid_dish)
async def test_get_calories_invalid_servings(mock_get):
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await get_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        for servings in [0, -1]:
            response = await client.post("/get-calories", json={
                "dish_name": "Apple",
                "servings": servings
            }, headers=headers)

            assert response.status_code in (400, 422)

