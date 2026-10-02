import pytest
import requests
import allure
from data import URLS, ENDPOINTS
import helpers

class TestCreationCourier:

   @allure.title("Проверка успешного создания курьера")   
   @allure.description("Создаём курьера с обязательными полями и запрос возвращает правильный код и текст ответа")
   def test_correct_response_create_new_courier(self, delete_courier_after_test):
      payload = {
            "login": helpers.new_login(),
            "password": helpers.new_password(),
            "firstName": "nina"
      }
      delete_courier_after_test["login"] = payload['login']
      delete_courier_after_test["password"] = payload['password']
      with allure.step("Отправка POST-запроса на создание курьера"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload)
         assert response.status_code == 201
         assert response.json() == {"ok": True}

   
   @allure.title("Проверка создания двух одинаковых курьеров")   
   @allure.description("Создаём курьера, после создания курьера с идентичными данными первого")
   def test_create_two_identical_couriers(self, new_courier, delete_courier_after_test):
      login, password, first_name = new_courier
      payload = {
        "login": login,
        "password": password,
        "firstName": first_name
      }
      delete_courier_after_test["login"] = login
      delete_courier_after_test["password"] = password
      with allure.step("Отправка POST-запроса на создание дублирующего курьера"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload)

         assert response.status_code == 409
         assert "Этот логин уже используется" in response.json()["message"]

   
   @allure.title("Проверка создания курьера без заполнения одного из полей")   
   @allure.description("Создаём курьера с двумя вариантами отсутствия одного из полей")
   @pytest.mark.parametrize("missing_field", ["login", "password"])
   def test_with_missing_field(self, missing_field, new_courier):
      login, password, first_name = new_courier
      
      payload = {
         "login": login,
         "password": password,
         "firstName": first_name
      }
      del payload[missing_field]

      with allure.step("Отправка POST-запроса на создание курьера без заполнения одного из полей"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload)

         assert response.status_code == 400
         assert "Недостаточно данных для создания учетной записи" in response.json()["message"]


   @allure.title("Проверка создания курьера с существующим логином")   
   @allure.description("Создаём одного курьера, далее создаём второго с идентичным логином, но с отличными другими данными")
   def test_create_identical_login(self, new_courier, delete_courier_after_test):
      login, password, _ = new_courier
      delete_courier_after_test["login"] = login
      delete_courier_after_test["password"] = password

      payload = {
        "login": login,
        "password": "4321",
        "firstName": "nina"
      }
      with allure.step("Отправка POST-запроса на создание курьера с существующим логином"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload)

         assert response.status_code == 409
         assert "Этот логин уже используется" in response.json()["message"]


class TestCourierLogin:

   @allure.title("Проверка успешной авторизации")   
   @allure.description("Авторизуемся зарегистрированными данными курьера, заполняя все обязательные поля")
   def test_successful_authorization(self, reg_courier, delete_courier_after_test):   
      payload = {
         "login": reg_courier["login"],
         "password": reg_courier["password"],
      }
      delete_courier_after_test["login"] = payload['login']
      delete_courier_after_test["password"] = payload['password']

      with allure.step("Отправка POST-запроса на авторизацию курьера"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

         assert response.status_code == 200
         assert "id" in response.json()


   @allure.title("Проверка авторизации при вводе неправильных данных")   
   @allure.description("Вводим данные для авторизации с двумя вариантами неправильно указанных логина/пароля")
   @pytest.mark.parametrize("field, wrong_value", [
    ("login", "courier"),
    ("password", "8888"),
])
   def test_wrong_login_or_pass(self, field, wrong_value, reg_courier):
      payload = {
         "login": reg_courier["login"],
         "password": reg_courier["password"],
      }
      payload[field] = wrong_value

      with allure.step("Отправка POST-запроса на авторизацию курьера с неправильными данными"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

         assert response.status_code == 404
         assert "Учетная запись не найдена" in response.json()["message"]


   @allure.title("Проверка авторизации без заполнения поля логина")   
   @allure.description("Вводим данные для авторизацию без указания логина")
   def test_login_missing_login_field(self, reg_courier): 
      payload = {
         "password": reg_courier["password"],
         }
      
      with allure.step("Отправка POST-запроса на авторизацию курьера без логина"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

         assert response.status_code == 400
         assert "Недостаточно данных для входа" in response.json()["message"]


   @allure.title("Проверка авторизации без заполнения поля пароль")   
   @allure.description("Вводим данные для авторизации без указания пароля, ожидаем код 504(баг)")
   def test_login_missing_password_field(self, reg_courier): 
      payload = {
         "login": reg_courier["login"],
         }
      
      with allure.step("Отправка POST-запроса на авторизацию курьера без пароля"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

         assert response.status_code == 504



   @allure.title("Проверка авторизации несуществующего пользователем")   
   @allure.description("Вводим данные незарегистрированного пользователя для авторизации")
   def test_nonexistent_login_pass(self):
      payload = {
         "login": helpers.new_login(),
         "password": helpers.new_password(),
      }

      with allure.step("Отправка POST-запроса на авторизацию незарегистрированного курьера"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

         assert response.status_code == 404
         assert "Учетная запись не найдена" in response.json()["message"]
