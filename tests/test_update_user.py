import pytest
import requests
import allure
from src.config import Config
from src import helpers
from src import data

class TestUpdateUser:
        
    @allure.title("Успешное изменение email, имени, пароля авторизованного пользователя")
    @pytest.mark.parametrize("key, value", [
        ("email", f"{helpers.generate_random_string(10)}@ya.ru"),
        ("name", helpers.generate_random_string(10)),
        ("password", helpers.generate_random_string(10))])
    def test_update_auth_user_info(self, key, value):
        token = helpers.register_new_user_and_return_token()

        body = {key: value}
        update_response = requests.patch (f"{Config.BASE_URL}/api/auth/user", json=body, headers={"Authorization": token})
        assert update_response.status_code == 200
        assert update_response.json()["success"] == True
        assert "user" in update_response.json()

        helpers.delete_user(token)
        
    @allure.title("Нельзя изменить email, имя, пароль неавторизованного пользователя")
    @pytest.mark.parametrize("key, value", [
        ("email", f"{helpers.generate_random_string(10)}@ya.ru"),
        ("name", helpers.generate_random_string(10)),
        ("password", helpers.generate_random_string(10))])
    def test_update_unauth_user_info(self, key, value):
        body = {key: value}
        update_response = requests.patch (f"{Config.BASE_URL}/api/auth/user", json=body)
        assert update_response.status_code == 401
        assert update_response.json()["success"] == False
        assert update_response.json()["message"] == data.message_unauth_user

    @allure.title("Нельзя передать почту которая уже используется")
    def test_update_user_email_alreadyused(self):
        token = helpers.register_new_user_and_return_token()

        body = {"email": data.LOGIN_EXIST_USER}
        update_response = requests.patch (f"{Config.BASE_URL}/api/auth/user", json=body, headers={"Authorization": token})
        assert update_response.status_code == 403
        assert update_response.json()["success"] == False
        assert update_response.json()["message"] == data.message_update_user_email_used

        helpers.delete_user(token)
