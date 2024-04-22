import requests
import json
import pymongo
# Задаем параметры прокси и аутентификации
proxy = {
    'http': 'http://nMuoL2:HTX1m6@64.226.55.115:8000',
    'https': 'http://nMuoL2:HTX1m6@64.226.55.115:8000'
}
# создал бд
db_client = pymongo.MongoClient("mongodb://localhost:27017")
project_db = db_client.project
raybet_db = project_db.raybet

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
# list_of_urls = list
# def append_url(url):
#     if url not in list_of_urls:
#         list_of_urls.append(url)
#     else:
#         print('Событие уже существует')
def creat_json(data):

    dict = {
    '_id': data['result']['id'], 
    'game_name': data['result']['game_name'],
    'match_name': data['result']['match_name'],
    'tournament_short_name': data['result']['tournament_short_name'],
    'odds': 
        {
            'Winner': {
                data['result']['odds'][0]['name']: data['result']['odds'][0]['odds'],
                data['result']['odds'][1]['name']: data['result']['odds'][1]['odds']
                },
            'Handicap':{
                data['result']['odds'][0]['name']+' '+data['result']['odds'][6]['value']:data['result']['odds'][6]['odds'],
                data['result']['odds'][1]['name']+' '+data['result']['odds'][7]['value']:data['result']['odds'][7]['odds']
            }
            }
    }

    raybet_db.insert_one(dict)


def get_data():
    try:
        response = requests.get('https://vncfgameinfo.365raylines.com/v2/odds?match_id=37943912', proxies=proxy)
        # Проверяем успешность запроса
        if response.status_code == 200:
            print("Запрос успешно отправлен через прокси.")
            print("Ответ от сервера:")
            data = response.json()
            creat_json(data)
        else:
            print(f"Произошла ошибка: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при отправке запроса: {str(e)}")
get_data()


# with open('test1.json', 'r',encoding="utf-8") as result_json:
#     json_data = json.load(result_json)
# print()
# print('Победа ',json_data['result']['odds'][0]['name'], 'общая - ',json_data['result']['odds'][0]['odds'],'кф')
# print('Победа ',json_data['result']['odds'][1]['name'], 'общая - ',json_data['result']['odds'][1]['odds'],'кф')
# print(json_data['result']['odds'][0]['name'], json_data['result']['odds'][6]['value'],json_data['result']['odds'][6]['odds'],'кф')
# print(json_data['result']['odds'][1]['name'], json_data['result']['odds'][7]['value'],json_data['result']['odds'][7]['odds'],'кф')
# print()

# with open('test2.json', 'r',encoding="utf-8") as result_json:
#     json_data = json.load(result_json)
# print()
# print('Победа ',json_data['result']['odds'][0]['name'], 'общая - ',json_data['result']['odds'][0]['odds'],'кф')
# print('Победа ',json_data['result']['odds'][1]['name'], 'общая - ',json_data['result']['odds'][1]['odds'],'кф')
# print(json_data['result']['odds'][0]['name'], json_data['result']['odds'][6]['value'],json_data['result']['odds'][6]['odds'],'кф')
# print(json_data['result']['odds'][1]['name'], json_data['result']['odds'][7]['value'],json_data['result']['odds'][7]['odds'],'кф')
# print()