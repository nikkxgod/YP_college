import requests
import json
import pymongo
from datetime import datetime
import time
import threading
import asyncio
from datetime import datetime, timedelta
# Задаем параметры прокси и аутентификации
proxy = {
    'http': 'http://L6rG3Y:UDAvqW@64.226.55.104:8000',
    'https': 'http://L6rG3Y:UDAvqW@64.226.55.104:8000'
}

import sqlite3


def delete_json(id):
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Match WHERE id = ?", (id,))
    cursor.execute("DELETE FROM Odds WHERE match_id = ?", (id,))
    cursor.execute("DELETE FROM Urls WHERE id = ?", (id,))
    cursor.close()
    

def create_json(data):
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
    print('зашел в create_json')
    now = datetime.now()
    start_time = datetime.strptime(data['result']['start_time'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5)
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
    elif data['result']['game_name']=='无尽对决':
        for i in data['result']['odds']:
            if i['match_stage']=='r1' and i['sort_index']==2879800:
                map1[i['name']]=i['odds']
            if i['match_stage']=='r2' and i['sort_index']==2878950:
                map2[i['name']]=i['odds']
    dict = {
        '_id': data['result']['id'], 
        'game_name': data['result']['game_name'],
        'match_name': data['result']['match_name'],
        'tournament_short_name': data['result']['tournament_short_name'],
        'start_time': start_time,
        'status':status[status_code],
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
    #добавляем в таблицу Match
    cursor.execute("INSERT INTO Match (id, game_name, match_name, tournament_short_name, start_time, status, round) VALUES (?, ?, ?, ?, ?, ?, ?)", (dict['_id'], dict['game_name'], dict['match_name'], dict['tournament_short_name'], dict['start_time'], dict['status'], dict['round'],))
    connection.commit()
    #team1 winner
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (dict['_id'], 'Winner', data['result']['odds'][0]['odds'], data['result']['odds'][0]['name'], now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    #team2 winner
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (dict['_id'], 'Winner', data['result']['odds'][1]['odds'], data['result']['odds'][1]['name'], now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    #team1 map1
    team_name = list(map1.items())[0][0]
    odd_value = list(map1.items())[0][1]
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (dict['_id'], 'Map 1', odd_value, team_name, now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    #team2 map1
    team_name = list(map1.items())[1][0]
    odd_value = list(map1.items())[1][1]
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (dict['_id'], 'Map 1', odd_value, team_name, now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    #team1 map2
    team_name = list(map2.items())[1][0]
    odd_value = list(map2.items())[1][1]
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (dict['_id'], 'Map 2', odd_value, team_name, now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    #team2 map2
    team_name = list(map2.items())[0][0]
    odd_value = list(map2.items())[0][1]
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (dict['_id'], 'Map 2', odd_value, team_name, now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    connection.close()

def update_data(data):
    print('зашел в update_data')
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
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
    elif data['result']['game_name']=='无尽对决':
        for i in data['result']['odds']:
            if i['match_stage']=='r1' and i['sort_index']==2879800:
                map1[i['name']]=i['odds']
            if i['match_stage']=='r2' and i['sort_index']==2878950:
                map2[i['name']]=i['odds']


    cursor.execute("Update Match SET status=? WHERE id=?",(status[status_code], data['result']['id']))
    #team1 winner
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (data['result']['id'], 'Winner', data['result']['odds'][0]['odds'], data['result']['odds'][0]['name'], now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    #team2 winner
    cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (data['result']['id'], 'Winner', data['result']['odds'][1]['odds'], data['result']['odds'][1]['name'], now.strftime("%d/%m/%Y %H:%M")))
    connection.commit()
    #team1 map1
    items = list(map1.items())
    first_pair = items[0]
    second_pair = items[1]
    if len(map1)>0:
        cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (data['result']['id'], 'Map 1', first_pair[1], first_pair[0], now.strftime("%d/%m/%Y %H:%M")))
        connection.commit()
        #team2 map1
        cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (data['result']['id'], 'Map 1', second_pair[1], second_pair[0], now.strftime("%d/%m/%Y %H:%M")))
        connection.commit()
      
    #team1 map2
    items = list(map2.items())
    first_pair = items[0]
    second_pair = items[1]
    if len(map1)>0:
        cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (data['result']['id'], 'Map 2', first_pair[1], first_pair[0], now.strftime("%d/%m/%Y %H:%M")))
        connection.commit()
        #team2 map2
        cursor.execute("INSERT INTO Odds (match_id, bet_type, odds_value, team, datetime) VALUES (?, ?, ?, ?, ?)", (data['result']['id'], 'Map 2', second_pair[1], second_pair[0], now.strftime("%d/%m/%Y %H:%M")))
        connection.commit()
    connection.close()
    

def get_data(id,there_is_flag):
    try:
        response = requests.get(f'https://vncfgameinfo.365raylines.com/v2/odds?match_id={id}', proxies=proxy)
        # Проверяем успешность запроса
        if response.status_code == 200:
            print("Запрос успешно отправлен через прокси.")
            print("Ответ от сервера:")
            data = response.json()
            if there_is_flag==False:
                create_json(data)
            else:
                update_data(data)
        else:
            print(f"Произошла ошибка: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при отправке запроса: {str(e)}")


def input_url(url):
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
    id = url.split('/')[-1]
    cursor.execute("SELECT id FROM Match WHERE id = ?", (id,))
    match_exists = cursor.fetchone()
    if match_exists:
        print('СОБЫТИЕ УЖЕ СУЩЕСТВУЕТ')
        there_is_flag = True
    else:
        print('СОБЫТИЯ НЕТ')
        there_is_flag = False
    connection.close()
    get_data(id,there_is_flag)


async def periodic_operation(interval):
    i = 0
    while True:
        list_of_urls = []
        connection = sqlite3.connect("project.db")
        cursor = connection.cursor()
        # Получение всех URL из таблицы Urls
        cursor.execute("SELECT url FROM Urls")
        urls = cursor.fetchall()
        cursor.close()
        
        # Если таблица Urls не пуста
        if urls:
            # Преобразуем список URL в Python-формат
            list_of_urls = [url[0] for url in urls]
            
            # Задержка между обновлениями
            await asyncio.sleep(interval)
            
            # Вызываем функцию обработки URL
            input_url(list_of_urls[i % len(list_of_urls)])
            print(f'Обновляется {list_of_urls[i % len(list_of_urls)]}')
            i += 1
        else:
            # Если нет URL, ждем и продолжаем проверять
            cursor.close()
            await asyncio.sleep(interval)

loop = asyncio.run(periodic_operation(2))

