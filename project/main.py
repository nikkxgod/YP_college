import requests
import json
import pymongo
from datetime import datetime
from bson.json_util import dumps
now = datetime.now()
import time
import threading
import asyncio

# создал бд
db_client = pymongo.MongoClient("mongodb://localhost:27017")
project_db = db_client.project
urls_db = project_db.urls

def append_url(url):
    id = int(url.split('/')[-1])
    urls_db.insert_one({
        '_id':id,
        'url':url
        })
append_url('https://rbvn3.com/match/37945562')