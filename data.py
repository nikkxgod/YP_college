import requests
import json
import pymongo
from datetime import datetime
from bson.json_util import dumps
import time
import threading
import asyncio
from datetime import datetime, timedelta
# Задаем параметры прокси и аутентификации
proxy = {
    'http': 'http://nMuoL2:HTX1m6@64.226.55.115:8000',
    'https': 'http://nMuoL2:HTX1m6@64.226.55.115:8000'
}
# создал бд
db_client = pymongo.MongoClient("mongodb://localhost:27017")
project_db = db_client.project
raybet_db = project_db.raybet
urls_db = project_db.urls

def delete_json(id):
    urls_db.delete_one({'_id':id})
    raybet_db.delete_one({'_id':id})
    

def creat_json(data):
    now = datetime.now()
    srart_time = datetime.strptime(data['result']['start_time'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5)
    map1 = {}
    map2 = {}
    status=['','prematch','live','end']
    status_code = data['result']['status']
    if status_code==3:
        print('Событие уже завершено')
        return
    if data['result']['game_name']=='CS2':
        for i in data['result']['odds']:
            if i['match_stage']=='map1' and i['odds_group_id']==16854:
                map1[i['name']]=i['odds']
            if i['match_stage']=='map2' and i['odds_group_id']==16877:
                map2[i['name']]=i['odds']
    elif data['result']['game_name']=='DOTA2':
        for i in data['result']['odds']:
            if i['match_stage']=='r1' and i['sort_index']==679550:
                map1[i['name']]=i['odds']
            if i['match_stage']=='r2' and i['sort_index']==674650:
                map2[i['name']]=i['odds']
    dict = {
        '_id': data['result']['id'], 
        'game_name': data['result']['game_name'],
        'match_name': data['result']['match_name'],
        'tournament_short_name': data['result']['tournament_short_name'],
        'start_time': srart_time,
        'Status':status[status_code],
        'round':data['result']['round'],
        'teams':[data['result']['team'][0]['team_name'],data['result']['team'][1]['team_name']],
        'odds':[{
                'Date time': f'{now.strftime("%d/%m/%Y %H:%M")}',
                'Winner': {
                    data['result']['odds'][0]['name']: data['result']['odds'][0]['odds'],
                    data['result']['odds'][1]['name']: data['result']['odds'][1]['odds']
                },
                'Map 1': map1,
                'Map 2': map2
            
        }]
        }
    raybet_db.insert_one(dict)

def update_data(data):
    now = datetime.now()
    map1 = {}
    map2 = {}
    status=['','prematch','live','end']
    status_code = data['result']['status']
    if status_code==3:
        delete_json(data['result']['id'])
        return
    if data['result']['game_name']=='CS2':
        for i in data['result']['odds']:
            if i['match_stage']=='map1' and i['odds_group_id']==16854:
                map1[i['name']]=i['odds']
            if i['match_stage']=='map2' and i['odds_group_id']==16877:
                map2[i['name']]=i['odds']
    elif data['result']['game_name']=='DOTA2':
        for i in data['result']['odds']:
            if i['match_stage']=='r1' and i['sort_index']==679550:
                map1[i['name']]=i['odds']
            if i['match_stage']=='r2' and i['sort_index']==674650:
                map2[i['name']]=i['odds']

    new_odds_data = {
            'Date time': f'{now.strftime("%d/%m/%Y %H:%M")}',
            'Winner': {
                data['result']['odds'][0]['name']: data['result']['odds'][0]['odds'],
                data['result']['odds'][1]['name']: data['result']['odds'][1]['odds']
            },
            'Handicap': {
                data['result']['odds'][0]['name'] + ' ' + data['result']['odds'][6]['value']: data['result']['odds'][6]['odds'],
                data['result']['odds'][1]['name'] + ' ' + data['result']['odds'][7]['value']: data['result']['odds'][7]['odds']
            },
            'Total map': {
                'Over 2.5': data['result']['odds'][9]['odds'],
                'Under 2.5': data['result']['odds'][8]['odds']
            },
            'Map 1': map1,
            'Map 2': map2
        }
    raybet_db.update_one({'_id':data['result']['id']},{'$set':{'Status':status[status_code]}})
    raybet_db.update_one({'_id':data['result']['id']},{'$push':{'odds':new_odds_data}})
    

def get_data(id,there_is_flag):
    try:
        response = requests.get(f'https://vncfgameinfo.365raylines.com/v2/odds?match_id={id}', proxies=proxy)
        # Проверяем успешность запроса
        if response.status_code == 200:
            print("Запрос успешно отправлен через прокси.")
            print("Ответ от сервера:")
            data = response.json()
            if there_is_flag==False:
                creat_json(data)
            else:
                update_data(data)
        else:
            print(f"Произошла ошибка: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при отправке запроса: {str(e)}")


def input_url(url):
    there_is_flag = True
    id = url.split('/')[-1]
    if raybet_db.find_one({'_id':int(id)})==None:
        there_is_flag = False
    get_data(id,there_is_flag)

async def periodic_operation(interval):
    i=0
    while True:
        list_of_urls = []
        collection_urls = urls_db.find()
        count_urls = urls_db.count_documents({})
        if count_urls>0:
            for collection in collection_urls:
                list_of_urls.append(collection['url'])
            await asyncio.sleep(interval)
            input_url(list_of_urls[i%len(list_of_urls)])
            print(f'обновляется {list_of_urls[i%len(list_of_urls)]}')
            i+=1
        else:
            continue

loop = asyncio.get_event_loop()
loop.run_until_complete(periodic_operation(1))

