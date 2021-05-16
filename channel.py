import os
import json
import websocket
from time import sleep
from multiprocessing import Process
from database import DataBase
from dotenv import load_dotenv; load_dotenv()

count = 0
online_count = 0
guild_id = os.getenv("guild_id")
channel_id = os.getenv("channel_id")
timeout = None
token = os.getenv("token")

def fetch():
    ws = websocket.WebSocketApp('wss://gateway.discord.gg/?encoding=json&v=8',
                                on_open=on_open, on_message=on_message)
    ws.run_forever()

def stop_chunk(ws):
    ws.send("close")

def on_open(ws):
    print("WebSocket connection established")
    Auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {}
        }
    }
    ws.send(json.dumps(Auth))

def on_message(ws, message):
    global count
    global online_count
    global timeout
    data = json.loads(message)

    if data['op'] == 0 and data['t'] == 'READY':
        print('Login successful')
        getUsers = {
            "op": 14,
            "d": {
                "guild_id": guild_id,
                "channels": { channel_id: [[0,99]] }
            }
        }
        ws.send(json.dumps(getUsers))
    elif data['op'] == 0 and data['t'] == 'GUILD_MEMBER_LIST_UPDATE':
        for op in data['d']['ops']:
            if op['op'] == 'SYNC':
                online_count = int(data['d']['online_count'])
                for item in op['items']:
                    try:
                        add(item['member']['user'])
                    except:
                        pass
                if count*100 <= online_count:
                    count += 1
                    print(f'Next range {count*100} - {(count*100)+99}')
                    getUsers = {
                        "op": 14,
                        "d": {
                            "guild_id": guild_id,
                            "channels": { channel_id: [[0,99], [count*100,(count*100)+99]] }
                        }
                    }
                    ws.send(json.dumps(getUsers))
                else:
                    #ws.send("close")
                    ws.send(json.dumps({"op":8,"d":{"guild_id":[guild_id],"query":"","limit":1000000,"presences":False}}))
                    timeout = Process(target=stop_chunk, args=(ws,))
                    timeout.start()
                    timeout.json(timeout=7)

    elif data['op'] == 0 and data['t'] == 'GUILD_MEMBERS_CHUNK':
        timeout.terminate()
        print("Getting members chunk...")
        for member in data['d']['members']:
            add(member['user'])

def add(user):
    id = user['id']
    if 'bot' not in user.keys() and not DataBase.Status(id):
        username = user['username']
        print(f"Adding {username} to database")
        newUser = DataBase(username, id, 1)
        newUser.GoToDB()