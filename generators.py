import requests
import random
import string
from data import URLS, ENDPOINTS


# метод регистрации нового курьера возвращает список из логина и пароля
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


#Метод генерации нового логина
def create_new_login():
    login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return login

#Метод генерации нового пароля
def create_new_password():
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return password