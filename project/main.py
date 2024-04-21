import requests
import json

# Задаем параметры прокси и аутентификации
proxy = {
    'http': 'http://nMuoL2:HTX1m6@64.226.55.115:8000',
    'https': 'http://nMuoL2:HTX1m6@64.226.55.115:8000'
}

# Отправляем GET-запрос на сайт через прокси
# try:
#     response = requests.get('https://vncfgameinfo.365raylines.com/v2/odds?match_id=37944713', proxies=proxy)
#     # Проверяем успешность запроса
#     if response.status_code == 200:
#         print("Запрос успешно отправлен через прокси.")
#         print("Ответ от сервера:")
#         res = response.json()
#         print(res['result']['odds'][0])
#     else:
#         print(f"Произошла ошибка: {response.status_code}")
# except Exception as e:
#     print(f"Произошла ошибка при отправке запроса: {str(e)}")

#start
list_of_urls = list
def append_url(url):
    if url not in list_of_urls:
        list_of_urls.append(url)
    else:
        print('Событие уже существует')

def get_data():
    try:
        response = requests.get('https://vncfgameinfo.365raylines.com/v2/odds?match_id=37944713', proxies=proxy)
        # Проверяем успешность запроса
        if response.status_code == 200:
            print("Запрос успешно отправлен через прокси.")
            print("Ответ от сервера:")
            res = response.json()
            print(res['result']['odds'][0]['odds'])
        else:
            print(f"Произошла ошибка: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при отправке запроса: {str(e)}")
get_data()