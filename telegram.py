import telebot
import asyncio
import pymongo
import time
bot = telebot.TeleBot('7159348995:AAE1Y_Ta2Ey9VPtPWiu6Vz5CIqRhOVbn1VI')
chat_id =  '-1002064549773'
def send_message(match_name,count_update):
    stroka = (f'В матче {match_name} происходит какая-то активность с коэффициентами\n'
              f'Количество изменений: {count_update}')
    bot.send_message(chat_id=chat_id, text=stroka)


db_client = pymongo.MongoClient("mongodb://localhost:27017")
project_db = db_client.project
raybet_db = project_db.raybet

event_dict = {}

def update_events():
    global event_dict
    events = raybet_db.find()
    for event in events:
        team_name1 = event['teams'][0]
        if event['round']=='bo3':
            event_id = event['_id']
            event_dict[event_id] = {}
            event_dict[event_id]['Winner'] = event['odds'][-1]['Winner'][team_name1]
            event_dict[event_id]['Map 1'] = event['odds'][-1]['Map 1'][team_name1]
            event_dict[event_id]['Map 2'] = event['odds'][-1]['Map 2'][team_name1]
            event_dict[event_id]['count_update'] = 0
        elif event['round']=='bo1':
            event_id = event['_id']
            event_dict[event_id] = {}
            event_dict[event_id]['Winner'] = event['odds'][-1]['Winner'][team_name1]
            event_dict[event_id]['count_update'] = 0


async def periodic_operation(interval):
    while True:
        global event_dict
        events = raybet_db.find()
        for event in events:
            if event['Status'] != 'prematch':
                continue
            event_id = event['_id']
            team_name1 = event['teams'][0]
            if event_id not in event_dict:  # Проверяем наличие ключа в словаре
                # Если ключ отсутствует, добавляем новую запись в словарь
                if event['round'] == 'bo3':
                    event_dict[event_id] = {
                        'Winner': event['odds'][-1]['Winner'][team_name1],
                        'Map 1': event['odds'][-1]['Map 1'][team_name1],
                        'Map 2': event['odds'][-1]['Map 2'][team_name1],
                        'count_update': 0
                    }
                elif event['round'] == 'bo1':
                    event_dict[event_id] = {
                        'Winner': event['odds'][-1]['Winner'][team_name1],
                        'count_update': 0
                    }
            else:
                if event['round'] == 'bo3':
                    winner = event['odds'][-1]['Winner'][team_name1]
                    map1 = event['odds'][-1]['Map 1'][team_name1]
                    map2 = event['odds'][-1]['Map 2'][team_name1]
                    if (event_dict[event_id]['Winner'] != winner or
                            event_dict[event_id]['Map 1'] != map1 or
                            event_dict[event_id]['Map 2'] != map2):
                        event_dict[event_id]['count_update'] += 1
                        send_message(event['match_name'], event_dict[event_id]['count_update'])
                        event_dict[event_id]['Winner'] = winner
                        event_dict[event_id]['Map 1'] = map1
                        event_dict[event_id]['Map 2'] = map2

                elif event['round'] == 'bo1':
                    winner = event['odds'][-1]['Winner'][team_name1]
                    if event_dict[event_id]['Winner'] != winner:
                        event_dict[event_id]['count_update'] += 1
                        send_message(event['match_name'], event_dict[event_id]['count_update'])
                        event_dict[event_id]['Winner'] = winner

update_events()
loop = asyncio.get_event_loop()
loop.run_until_complete(periodic_operation(1))

