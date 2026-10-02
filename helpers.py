import requests
import allure
from generators import create_new_login, create_new_password
from data import URLS, ENDPOINTS


# Создание нового логина
def new_login():
   return create_new_login()
    
# Создание нового пароля
def new_password():
   return create_new_password()

# Получение ID курьера
def login_and_get_id(login, password):
   response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data={"login":login, "password":password})
   return response.json().get("id")

# Отправка DELETE-запроса на удаление курьера
def delete_courier(courier_id):
   if courier_id:
      requests.delete(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_DELETE_COURIER}{courier_id}')


