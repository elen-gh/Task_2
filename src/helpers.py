import random
import string
import requests
from src.config import Config
from src import data

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def register_new_user_and_return_token():
    
    payload = {
        "email": f"{generate_random_string(10)}@ya.ru",
        "password": generate_random_string(10),
        "name": generate_random_string(10)
    }
    response = requests.post(f"{Config.BASE_URL}/api/auth/register", json=payload)
    return response.json().get("accessToken")

def auth_user_and_return_token():
    body = {
        "email": data.LOGIN_EXIST_USER,
        "password": data.PASSWORD_EXIST_USER
    }
    response = requests.post (f"{Config.BASE_URL}/api/auth/login", json=body)
    return response.json().get("accessToken")

def delete_user(token):
    return requests.delete(f"{Config.BASE_URL}/api/auth/user", headers={"Authorization": token})