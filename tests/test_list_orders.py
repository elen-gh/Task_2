import requests
import allure
from src.config import Config
from src import helpers
from src import data

class TestListOrders:

    @allure.title("Получение списка заказов авторизованного пользователя")
    def test__authorised_user_list_orders_(self):
        token = helpers.auth_user_and_return_token()
        list_response = requests.get (f"{Config.BASE_URL}/api/orders", headers={"Authorization": token})
        
        assert list_response.status_code == 200
        assert list_response.json()["success"] == True
        assert "orders" in list_response.json()

    @allure.title("Получение списка заказов неавторизованного пользователя")
    def test_unauth_user_list_orders(self):
        
        list_response = requests.get (f"{Config.BASE_URL}/api/orders")
        assert list_response.status_code == 401
        assert list_response.json()["success"] == False
        assert list_response.json()["message"] == data.message_unauth_user

