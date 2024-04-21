import requests

# Задаем параметры прокси и аутентификации
proxy = {
    'http': 'http://nMuoL2:HTX1m6@64.226.55.115:8000',
    'https': 'http://nMuoL2:HTX1m6@64.226.55.115:8000'
}

# Отправляем GET-запрос на сайт через прокси
try:
    response = requests.get('https://vncfgameinfo.365raylines.com/v2/odds?match_id=37944713', proxies=proxy)
    # Проверяем успешность запроса
    if response.status_code == 200:
        print("Запрос успешно отправлен через прокси.")
        print("Ответ от сервера:")
        print(response.json())
    else:
        print(f"Произошла ошибка: {response.status_code}")
except Exception as e:
    print(f"Произошла ошибка при отправке запроса: {str(e)}")
