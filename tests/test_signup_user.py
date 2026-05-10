import pytest
import requests
import allure
from src.config import Config
from src import data
from src import helpers

class TestSignupUser:
        
    @allure.title("Успешное создание пользователя")
    def test_signup_user_valid(self):
        body = {
    "email": f"{helpers.generate_random_string(10)}@ya.ru",
    "password": helpers.generate_random_string(10),
    "name": helpers.generate_random_string(10)
    }
        signup_response = requests.post (f"{Config.BASE_URL}/api/auth/register", json=body)
        assert signup_response.status_code == 200
        assert signup_response.json()["success"] == True
        assert "accessToken" in signup_response.json()
        assert "refreshToken" in signup_response.json()
        assert "user" in signup_response.json()

        token = signup_response.json()["accessToken"]
        helpers.delete_user(token)

    @allure.title("Cоздание пользователя с недостающими данными")
    @pytest.mark.parametrize("email, password, name", [
        ("", helpers.generate_random_string(10), helpers.generate_random_string(10)),
        (f"{helpers.generate_random_string(10)}@ya.ru", helpers.generate_random_string(10), ""),
        (f"{helpers.generate_random_string(10)}@ya.ru", "", helpers.generate_random_string(10))
    ])

    def test_login_user_missing_data(self, email, password, name):
        body = {
            "email": email,
            "password": password,
            "name": name
        }
        signup_response = requests.post (f"{Config.BASE_URL}/api/auth/register", json=body)
        assert signup_response.status_code == 403
        assert signup_response.json()["success"] == False
        assert signup_response.json()["message"] == data.message_signup_missing_data

    @allure.title("Нельзя создать двух одинаковых пользователей")
    def test_signup_user_double(self):
        body = {
        "email": data.LOGIN_EXIST_USER,
        "password": data.PASSWORD_EXIST_USER,
        "name": data.NAME_EXIST_USER
        }
        signup_response = requests.post (f"{Config.BASE_URL}/api/auth/register", json=body)
        assert signup_response.status_code == 403
        assert signup_response.json()["success"] == False
        assert signup_response.json()["message"] == data.message_signup_user_double

   