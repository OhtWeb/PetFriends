from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()
#1 Тест получения ключа с верными данными
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status_code, res = pf.get_api_key(email, password)
    assert status_code == 200
    assert 'key' in res

#2 Тест получения ключа с неверными данными (email)
def test_get_api_key_for_invalid_user_email(email=None, password=valid_password):
    status_code, res = pf.get_api_key_wrong_data(email, password)
    assert status_code == 403
    assert 'key' not in res

#3 Тест получения ключа с неверными данными (password)
def test_get_api_key_for_invalid_user_pass(email=valid_email, password=None):
    status_code, res = pf.get_api_key_wrong_data(email, password)
    assert status_code == 403
    assert 'key' not in res

#4 Тест получения всех животных с верным ключом
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status_code, result = pf.get_list_of_pets(auth_key, filter)
    assert status_code == 200
    assert len(result['pets']) > 0

#5 Тест получения всех животных с неверным ключом
def test_get_all_pets_with_wrong_key(filter=''):
    auth_key = {'key': '12345abcde_wrong_key'}
    status_code, result = pf.get_list_of_pets_wrong_key(auth_key, filter)
    assert status_code == 403

#6 Тест добавления нового питомца
def test_add_new_pet_simple():
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # получаем ключ
    # Передаем данные животного в метод
    result, status = pf.post_new_pet(auth_key, 'Барсик', 'Кот', '2')

    assert status == 200
    # Проверяем, верно ли добавились поля:
    assert result['name'] == 'Барсик'
    assert result['animal_type'] == 'Кот'
    assert result['age'] == '2'

#7 Тест добавления нового питомца c неполными данными
def test_add_new_pet_simple_unfilled():
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # получаем ключ
    # Передаем данные животного в метод
    result, status = pf.post_new_pet(auth_key, '', '', '')
    if status == 200:
        print(f"\nСервер позволяет создание питомца без атрибутов с ID: {result['id']}")
    # Это очевидная ошибка (должно быть 400)
    assert status != 200, "Сервер не должен создавать питомца без имени, типа и возраста!"

#8 Тест добавления нового питомца c абсурдными данными
def test_add_new_pet_simple_nonsense():
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # получаем ключ
    # Передаем данные животного в метод
    result, status = pf.post_new_pet(auth_key, 'Loremipsumdolorsitametconsecteturadipiscingelitsed', '12345678910', '-28')
    if status == 200:
        print(f"\nСервер позволяет создание питомца при вводе в поля атрибутов заведомо абсурдных данных с ID: {result['id']}")
    # Это очевидная ошибка (должно быть 400/403) - нужно добавить в поля ввода фильтры для типа и длины вводимой информации
    assert status != 200

#9 Тест добавления фото
def test_add_pet_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список только СВОИХ питомцев
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    # Если питомцев нет - создаем одного, чтобы тест не падал
    if len(result['pets']) == 0:
        pf.post_new_pet(auth_key, "Temporary", "cat", "1")
        _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][0]['id']
    # Получим путь к папке с test_pet_friends
    current_dir = os.path.dirname(__file__)
    img_path = os.path.join(current_dir, 'images', 'cat.jpg')
    # Проверим, найдется ли файл
    print(f"\nИщем файл по адресу: {img_path}")

    # Передаем абсолютный путь в метод
    status, result = pf.add_photo_to_pet(auth_key, pet_id, img_path)

    assert status == 200
    assert result['pet_photo'] != ""

#10 Тест добавления вместо фото файла неподдерживающегося формата
def test_add_photo_invalid_file_type():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список только СВОИХ питомцев
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    # Если питомцев нет - создаем одного, чтобы тест не падал
    if len(result['pets']) == 0:
        pf.post_new_pet(auth_key, "Temporary", "cat", "1")
        _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][0]['id']
    # Получим путь к папке с test_pet_friends
    current_dir = os.path.dirname(__file__)
    img_path = os.path.join(current_dir, 'images', 'notacat.txt')
    # Проверим, найдется ли файл
    print(f"\nИщем файл по адресу: {img_path}")

    # Передаем абсолютный путь в метод
    status, result = pf.add_photo_to_pet(auth_key, pet_id, img_path)
    if status == 200:
        print('Сервер вместо изображения принял текстовый файл')
    assert status != 200

#11 Тест добавления информации о питомце
def test_add_info_to_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Повторяем поиск файла
    current_dir = os.path.dirname(__file__)
    img_path = os.path.join(current_dir, 'images', 'pup.JPG')
    print(f"\nИщу файл по адресу: {img_path}")
    status, result = pf.add_info_to_pet(auth_key, 'Цербер', 'Песик', '3', img_path)
    assert status == 200
    assert result['pet_photo'] != ""
    assert result['name'] == 'Цербер'
    assert result['animal_type'] == 'Песик'
    assert result['age'] == '3'

#12 Тест обновления информации о питомце
def test_update_pet_info():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    # Если питомцев нет - создаем одного, чтобы тест не падал
    if len(result['pets']) == 0:
        pf.post_new_pet(auth_key, "Temporary", "cat", "1")
        _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    # Берем последнего питомца
    pet_id = result['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, 'Булка', 'Носорог', '18')
    assert status == 200
    assert result['name'] == 'Булка'
    assert result['animal_type'] == 'Носорог'
    assert result['age'] == '18'

#13 Тест удаления своего питомца
def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    # Если питомцев нет - создаем одного, чтобы тест не падал
    if len(result['pets']) == 0:
        pf.post_new_pet(auth_key, "Temporary", "cat", "1")
        _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    # Берем последнего питомца
    pet_id = result['pets'][0]['id']
    # Удаляем его
    status, result = pf.delete_pet(auth_key, pet_id)
    # Проверяем ответ сервера
    assert status == 200
    # Проверяем, точно ли удален питомец. Запрашиваем список питомцев СНОВА
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    # Ищем удаленный pet_id в новом списке
    pet_ids = [pet['id'] for pet in result['pets']]
    # Проверяем, что нашего ID больше нет в списке
    assert pet_id not in pet_ids
    print(f"\nПитомец с ID {pet_id} был удален.")

#14 Тест удаления чужого питомца
def test_delete_not_my_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Берем список всех животных
    _, all_pets = pf.get_list_of_pets(auth_key, filter='')
    # Берем список СВОИХ (чтобы точно не удалить своего)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    my_ids = [pet['id'] for pet in my_pets['pets']]
    # Находим чужого питомца
    foreign_pet_id = None
    for pet in all_pets['pets']:
        if pet['id'] not in my_ids:
            foreign_pet_id = pet['id']
            break
    # Если питомца нет:
    if not foreign_pet_id:
        pytest.skip("Чужие питомцы не найдены")
    # Удаляем чужого питомца
    status, _ = pf.delete_pet(auth_key, foreign_pet_id)
    # Проверяем ответ сервера
    assert status != 200,        \
        (print(
        f"\nСервер разрешил удаление чужого питомца! "
        f"\nID удаленного животного: {foreign_pet_id}"
        f"\nСтатус ответа: {status} (Ожидалось 403)"
    ))

#15 Проверка работы фильтра my_pets
def test_add_new_pet_and_check_count_increment():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем начальное количество моих питомцев
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    initial_count = len(result['pets'])
    # Добавляем нового
    pf.post_new_pet(auth_key, "IncrementTest", "Robot", "100")
    # Получаем новое количество
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    final_count = len(result['pets'])
    # 4. Проверяем инкремент
    assert final_count == initial_count + 1, (
        f"Ошибка инкремента! Было: {initial_count}, стало: {final_count}. "
        "Питомец не добавился в список 'my_pets'"
    )