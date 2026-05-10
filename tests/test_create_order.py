import pytest
import requests
import allure
from src.config import Config
from src import helpers
from src import data

class TestCreateOrder:

    @allure.title("Создание заказа  авторизованным пользователем")
    def test_create_order_auth_user(self):
        token = helpers.auth_user_and_return_token()
        
        body = {"ingredients": [data.VALID_INGREDIENT]}
        create_response = requests.post (f"{Config.BASE_URL}/api/orders", json=body, headers={"Authorization": token})
        assert create_response.status_code == 200
        assert create_response.json()["success"] == True
        assert "name" in create_response.json()
        assert "order" in create_response.json()
        
    @allure.title("Создание заказа с неверным хешем ингредиентов авторизованным пользователем")
    def test_create_order_invalidhash_ingredient_auth_user(self):
        token = helpers.auth_user_and_return_token()
        
        body = {"ingredients": [data.INVALID_INGREDIENT]}
        create_response = requests.post (f"{Config.BASE_URL}/api/orders", json=body, headers={"Authorization": token})
        assert create_response.status_code == 500
        
    @allure.title("Создание заказа без ингридиентов авторизованным пользователем")
    def test_create_order_no_ingredients_auth_user(self):
        token = helpers.auth_user_and_return_token()
        
        body = {"ingredients": []}
        create_response = requests.post (f"{Config.BASE_URL}/api/orders", json=body, headers={"Authorization": token})
        assert create_response.status_code == 400
        assert create_response.json()["success"] == False
        assert create_response.json()["message"] == data.message_create_order_auth_user_no_ingredient

    @allure.title("Создание заказа  неавторизованным пользователем")
    def test_create_order_unauth_user(self):
        body = {"ingredients": [data.VALID_INGREDIENT]}
        create_response = requests.post (f"{Config.BASE_URL}/api/orders", json=body)
        assert create_response.status_code == 401
        assert create_response.json()["success"] == False
        assert create_response.json()["message"] == data.message_unauth_user
