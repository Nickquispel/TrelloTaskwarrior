import requests
import json
import uuid
import subprocess
import config
import sys
import os


trelloapi = config.config['TRELLO']
wantedlist = config.config['TRELLO']['LISTS']


def getlists() :
    url = f"https://api.trello.com/1/boards/{trelloapi['BOARD']}/lists?key={trelloapi['API_KEY']}&token={trelloapi['API_TOKEN']}"
    response = requests.get(url)
    jsondata = json.loads(response.content)
    return jsondata

def getcards(lists) :
    for list in lists :
        if list['name'] in wantedlist : 
            listid = list['id']
            url = f"https://api.trello.com/1/lists/{listid}/cards?key={trelloapi['API_KEY']}&token={trelloapi['API_TOKEN']}"

            response = requests.get(url)

            jsondata = json.loads(response.content)
            return jsondata

def createjson(dict) :
    f = open("taskwarrior.json", "w")
    f.write(json.dumps(dict))
    f.close()

def importjson() :
    command = "task import "+ os.getcwd() +"/taskwarrior.json"
    process = subprocess.Popen(command.split())
            
def importcards(cards) :
        for card in cards :
            dict = {
                "description":card['name'],
                "status":'pending',
                "uuid": uuid.uuid3(uuid.NAMESPACE_DNS,card['id']).__str__()
            }

            createjson(dict)
            importjson()        



lists = getlists()
cards = getcards(lists)
importcards(cards)



