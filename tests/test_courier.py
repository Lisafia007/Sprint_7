import pytest
import requests
import allure
from data import URLS, ENDPOINTS


class TestCreationCourier:

   @allure.title("Проверка успешного создания курьера")   
   @allure.description("Создаём курьера с обязательными полями и запрос возвращает правильный код и текст ответа")
   def test_correct_response_create_new_courier(self, created_courier):
      response = created_courier
      
      assert response.status_code == 201
      assert response.json() == {"ok": True}

   
   @allure.title("Проверка создания двух одинаковых курьеров")   
   @allure.description("Создаём первого курьера, после создаёмвторого курьера с идентичными данными первого")
   def test_create_two_identical_couriers(self, new_courier):
      login, password, first_name = new_courier

      payload = {
        "login": login,
        "password": password,
        "firstName": first_name
      }
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

      response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload)

      assert response.status_code == 400
      assert "Недостаточно данных для создания учетной записи" in response.json()["message"]


   @allure.title("Проверка создания курьера с существующим логином")   
   @allure.description("Создаём одного курьера, далее создаём второго с идентичным логином, но с отличными другими данными")
   def test_create_identical_login(self, new_courier):

      ident_log = new_courier[0]

      payload = {
        "login": ident_log,
        "password": "4321",
        "firstName": "nina"
     }
      response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload)

      assert response.status_code == 409
      assert "Этот логин уже используется" in response.json()["message"]


class TestCourierLogin:

   @allure.title("Проверка успешной авторизации")   
   @allure.description("Авторизуемся зарегистрированными данными курьера, заполняя все обязательные поля")
   def test_successful_authorization(self, reg_courier):   
      payload = {
         "login": reg_courier["login"],
         "password": reg_courier["password"],
      }

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

      response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

      assert response.status_code == 404
      assert "Учетная запись не найдена" in response.json()["message"]


   @allure.title("Проверка авторизации без заполнения одного из полей")   
   @allure.description("Вводим данные для авторизации с двумя вариантами отсутсвуюшего поля логина/пароля")
   @pytest.mark.parametrize("missing_field", ["login", "password"])
   def test_with_missing_field(self, missing_field, reg_courier): 
      login = reg_courier["login"]   
      password = reg_courier["password"] 

      payload = {
         "login": login,
         "password": password,
         }
      del payload[missing_field]

      response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

      assert response.status_code in (400, 504)

      if response.status_code == 400:
         assert "Недостаточно данных для входа" in response.json()["message"]


   @allure.title("Проверка авторизации несуществующим пользователем")   
   @allure.description("Вводим данные незарегистрированного пользователя для авторизации")
   def test_nonexistent_login_pass(self, new_login, new_password):

      payload = {
         "login": new_login,
         "password": new_password
      }

      response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data=payload)

      assert response.status_code == 404
      assert "Учетная запись не найдена" in response.json()["message"]