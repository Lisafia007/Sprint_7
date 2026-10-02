import pytest
import requests
import allure
import json
from data import URLS, ENDPOINTS, DATA_SET

class TestOrderCreation:

   @allure.title("Проверка успешного создания заказа с указанием одного цвета")   
   @allure.description("Создаём заказ с указаниями двумя вариантами цвета BLACK или GREY")
   @pytest.mark.parametrize("colors", ["BLACK", "GREY"])
   def test_create_order_one_color(self, colors):
      payload = DATA_SET.copy()
      payload["color"] = [colors]

      with allure.step("Отправка POST-запроса на создание заказа с одним цветом"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_ORDER}', data=json.dumps(payload))

         assert response.status_code == 201
         assert "track" in response.json() 


   @allure.title("Проверка успешного создания заказа с указанием двух цветов")   
   @allure.description("Создаём заказ с указанием двух цветов BLACK и GREY")
   def test_create_order_two_colors(self):
      payload = DATA_SET.copy()
      payload["color"] = ["BLACK", "GREY"]
      with allure.step("Отправка POST-запроса на создание заказа с двумя цветами"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_ORDER}', data=json.dumps(payload))
      
         assert response.status_code == 201
         assert "track" in response.json()


   @allure.title("Проверка успешного создания заказа без указания цвета")   
   @allure.description("Создаём заказ без указания цвета")
   def test_create_order_colorless(self):      
      payload = DATA_SET.copy()
      payload["color"] = []

      with allure.step("Отправка POST-запроса на создание заказа без указания цвета"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_ORDER}', data=json.dumps(payload))
            
         assert response.status_code == 201
         assert "track" in response.json()


class TestOrderList:

   
   @allure.title("Проверка успешного получения списка заказов курьера")   
   @allure.description("Получаем список заказов созданного курьера по его id")
   def test_order_list_courier_id(self, courier_id):

      with allure.step("Отправка GET-запроса на получение списка заказов по id курьера"):
         response = requests.get(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_ORDER}{ENDPOINTS.ENDPOINT_ORDERS_COURIER}{courier_id}')

         assert response.status_code == 200
         assert "orders" in response.json()

   
   @allure.title("Проверка успешного получения списка заказов")   
   @allure.description("Получаем список из 10 заказов, доступных для взятия курьером")
   def test_list_available_orders(self):

      with allure.step("Отправка GET-запроса на получение списка из 10 заказов"):
         response = requests.get(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_10_AVAILABLE_ORDERS}')

         assert response.status_code == 200


   @allure.title("Проверка получения списка заказов несуществующего курьера")   
   @allure.description("Получаем список заказов по несуществующему id курьера")
   def test_nonexistent_courierId(self):
      nonexistent_id = 0

      with allure.step("Отправка GET-запроса на получение списка заказов по несуществующему id курьера"):
         response = requests.get(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_ORDER}{ENDPOINTS.ENDPOINT_ORDERS_COURIER}{nonexistent_id}')

         assert response.status_code == 404
         assert f"Курьер с идентификатором {nonexistent_id} не найден" in response.json()["message"]
