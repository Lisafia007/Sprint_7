import pytest
from generators import register_new_courier_and_return_login_password
from helpers import login_and_get_id, delete_courier

# Фикстура регистрации нового курьера, получении список из логина и пароля 
@pytest.fixture
def new_courier():
   login_pass =  register_new_courier_and_return_login_password()
   return login_pass

# Фикстура возвращает словарь с данными зарегистрированного курьера
@pytest.fixture
def reg_courier(new_courier):
   login, password, _ = new_courier
   return {"login":login, "password":password}

# Фикстура авторизации и возвращения id курьера
@pytest.fixture
def courier_id(new_courier):
   login, password, _ = new_courier
   return login_and_get_id(login, password)

# Фикстура удаляет созданного в тесте курьера
@pytest.fixture
def delete_courier_after_test():
   courier_to_delete = {}
    
   yield courier_to_delete
    
   if "login" in courier_to_delete and "password" in courier_to_delete:
      courier_id = login_and_get_id(courier_to_delete["login"], courier_to_delete["password"])
      if courier_id:
         delete_courier(courier_id)
   


    
