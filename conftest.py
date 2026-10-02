import pytest
import requests
import json
from generators import register_new_courier_and_return_login_password, create_new_login, create_new_password
from data import URLS, ENDPOINTS, DATA_SET

# Вспомогательная функция для авторизации и возвращения id курьера
def _login_and_get_id(login, password):
   response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_COURIER_LOGIN}', data={"login":login, "password":password})

   return response.json().get("id")

# Вспомогательная функция для удаления курьера по id
def _delete_courier(courier_id):
   if courier_id:
      requests.delete(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_DELETE_COURIER}{courier_id}')

# Фикстура для регистрации нового курьера, полученим список из логина и пароля. Удаляет после теста 
@pytest.fixture
def new_courier():
   login_pass =  register_new_courier_and_return_login_password()
   yield login_pass

   if login_pass:
      courier_id = _login_and_get_id(login_pass[0], login_pass[1])
      _delete_courier(courier_id)

# Фикстура для создания нового логина 
@pytest.fixture
def new_login():
   return create_new_login()
    
# Фикстура для создания нового пароля
@pytest.fixture
def new_password():
   return create_new_password()

# Фикстура для создания курьера
@pytest.fixture
def created_courier(new_login, new_password):
   payload = {
      "login": new_login,
      "password": new_password,
      "firstName": "nina"
   }
   response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_COURIER}', data=payload
   )
   yield response

   courier_id = _login_and_get_id(new_login, new_password)
   _delete_courier(courier_id)
    
# Зарегистрированный курьер 
@pytest.fixture
def reg_courier(new_courier):
   login, password, _ = new_courier
   return {"login":login, "password":password}

# Фикстура для получения id курьера
@pytest.fixture
def courier_id(new_courier):
   login, password, _ = new_courier
   return _login_and_get_id(login, password)

# Фикстура для создания зказа и отмены его после теста
@pytest.fixture
def created_order():
   created_tracks = []

   def _create_order(color):
      payload = DATA_SET.copy()
      payload["color"] = color
      response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_ORDER}', data=json.dumps(payload))
      track = response.json().get("track")
    
      if track:
         created_tracks.append(track)
      return response       

   yield _create_order

   for track in created_tracks:
      requests.put(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CANCEL_ORDER}',data={"track": track})
   



    
