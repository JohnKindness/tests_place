import requests
from bs4 import BeautifulSoup
import pytest


def test_basket_api():
    session = requests.Session()

    # URL-ы для входа и API
    login_url = 'http://127.0.0.1:8000/login/'
    api_url = 'http://127.0.0.1:8000/api/cart/'

    # Получаем страницу логина для извлечения CSRF-токена
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.content, 'html.parser')

    # Извлекаем CSRF-токен
    csrf_token_tag = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_token_tag:
        csrf_token = csrf_token_tag['value']
    else:
        print("Не удалось найти CSRF-токен на странице логина.")
        exit()

    # Ваши учетные данные
    payload = {
        'username': 'admin',
        'password': 'mainadmin123',
        'csrfmiddlewaretoken': csrf_token
    }

    # Заголовки, включая Referer
    headers = {
        'Referer': login_url
    }

    # Выполняем POST-запрос для аутентификации
    login_response = session.post(login_url, data=payload, headers=headers)

    # Проверяем, успешен ли вход
    if login_response.ok and login_response.url != login_url:
        print("Успешный вход!")
    else:
        print("Ошибка при входе.")
        print("Текст ответа при входе:")
        print(login_response.text)
        exit()

    # Делаем запрос к API продуктов
    response = session.get(api_url)

    # Делаем запрос к API продуктов
    response = session.get(api_url)

    # Делаем запрос к API корзины
    api_url = 'http://127.0.0.1:8000/api/cart/'
    response = session.get(api_url)

    if response.ok:
        data = response.json()
        cart_items = data.get('cart_items', [])
        for item in cart_items:
            print(f"Товар: {item['name']}, Цена: {item['price']}, Количество NEEWWW: {item['quantity']}")
    else:
        print("Ошибка при доступе к API корзины.")
        print(f"Статус-код ответа: {response.status_code}")
        print("Текст ответа API:")
        print(response.text)


test_basket_api()