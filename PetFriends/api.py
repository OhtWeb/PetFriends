import requests

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    #1 Получение пользовательского ключа
    def get_api_key(self, email, password):
        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"Ошибка {status_code}: {res.text}")
        try:
            res = res.json()
        except:
            res = res.text
        return status_code, res

    #2 Получение списка питомцев
    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status_code = res.status_code
        if res.status_code != 200:
            raise Exception(f"Ошибка {status_code}: {res.text}")
        try:
            res = res.json()
        except:
            res = res.text
        return status_code, res

    #3 Создание нового питомца
    def post_new_pet(self, auth_key, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        # Сбор данных о питомце:
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"Ошибка {status_code}: {res.text}")
        return res.json(), status_code

    #4 Добавление фото питомца
    def add_photo_to_pet(self, auth_key, pet_id, pet_photo):
        headers = {'auth_key': auth_key['key']}
        files = {
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        }
        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, files=files)

        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"Ошибка {status_code}: {res.text}")
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    #5 Добавление информации о питомце
    def add_info_to_pet(self, auth_key, name, animal_type, age, pet_photo):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        files = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=files)

        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"Ошибка {status_code}: {res.text}")
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    #6 Обновление информации о питомце
    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)

        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"Ошибка {status_code}: {res.text}")
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    #7 Удаление питомца
    def delete_pet(self, auth_key, pet_id):
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)

        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"Ошибка {status_code}: {res.text}")
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    """
    #1A Получение ключа с неверными пользовательскими данными. 
    Этот и следующий методы добавлены, потому что методы 1 и 2 просто не дадут совершить ошибку 
    и прервут выполнение теста еще на стадии получения responcе !=200
    """
    def get_api_key_wrong_data(self, email, password):
        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status_code = res.status_code

        # Блок if status_code != 200: raise Exception удален
        # теперь функция просто возвращает то, что пришло от сервера.

        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    #2A Получение списка животных с неверным ключом
    def get_list_of_pets_wrong_key(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status_code = res.status_code
        # Блок if status_code != 200: raise Exception удален
        # теперь функция просто возвращает то, что пришло от сервера.
        try:
            res = res.json()
        except:
            res = res.text
        return status_code, res