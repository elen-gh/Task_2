import pytest
import requests
import allure
from src.config import Config
from src import helpers
from src import data

class TestLoginUser:

    @allure.title("Логин пользователя валидные данные")
    def test_login_user_valid_data(self):
        body = {
    "email": data.LOGIN_EXIST_USER,
    "password": data.PASSWORD_EXIST_USER
    }
        login_response = requests.post (f"{Config.BASE_URL}/api/auth/login", json=body)
        assert login_response.status_code == 200
        assert login_response.json()["success"] == True
        assert "accessToken" in login_response.json()
        assert "refreshToken" in login_response.json()
        assert "user" in login_response.json()

    @allure.title("Логин пользователя невалидные данные")
    @pytest.mark.parametrize("email, password", [
        (data.LOGIN_EXIST_USER, data.PASSWORD_INVALID),
        (data.LOGIN_INVALID, data.PASSWORD_EXIST_USER),
        (f"{helpers.generate_random_string(10)}@ya.ru", helpers.generate_random_string(10)) 
    ])
    def test_login_user_invalid_data(self, email, password):
        body = {
            "email": email,
            "password": password
        }
        login_response = requests.post(f"{Config.BASE_URL}/api/auth/login", json=body)

        assert login_response.status_code == 401
        assert login_response.json()["success"] == False
        assert login_response.json()["message"] == data.message_login_user_invalid_data