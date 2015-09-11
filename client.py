import urllib.request as request
import urllib.parse as parse
from parser import *
import json
from time import sleep

# Servers address
mothership = 'http://192.241.194.12:8888/'

# HEADERS
headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'
}

# GET request function
def get(url):
    try:
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req, timeout=2)
        
        return { 
            'ok': True,
            'URLMatch': url == resp.url,
            'data': resp.read().decode('utf-8')
        }
    except Exception as e:
        return { 'ok': False, 'error': str(e)}

# POST request function
def post(url, values):
    try:
        data = parse.urlencode(values)
        data = data.encode('utf-8')

        req = request.Request(url, data, headers=headers)
        resp = request.urlopen(req, timeout=2)
        
        return { 
            'ok': True,
            'URLMatch': url == resp.url,
            'data': resp.read().decode('utf-8')
        }
    except Exception as e:
        return { 'ok': False, 'error': str(e)}

# Range bruteforce
def bruteforceRange(r):
    games = []
    for appid in r:
        url = 'http://store.steampowered.com/app/' + str(appid)
        data = get(url)
        if data['ok']:
            if data['URLMatch']:
                precook = prepare(data['data'])
                if precook:
                    print('Doing', url)
                    dish = cook(precook)
                    games.append(dish)
                else:
                    print('Skipping', url)
            else:
                print('Skipping', url)
        else:
            print('Skipping', url)

    return games

def StartClient():
    print('Starting client...')
    while True:
        task = ''
        try:
            task = get(mothership)
        except:
            print('Server is down')
            sleep(1)
            continue

        if task['ok']:
            try:
                todo = json.loads(task['data'])
                if 'start' in todo and 'stop' in todo and 'step' in todo:
                    print('Received task:', todo['start'], 'to', todo['stop'], 'step', todo['step'] )
                    r = range(todo['start'], todo['stop'], todo['step'])
     
                    data = bruteforceRange(r)
                    post(mothership, {'method': 'data', 'data' : json.dumps(data)})
                else:
                    print('No task')
                    sleep(1)
            except:
                print('No task')
        else:
            print('Failed to receive task')
        sleep(1)

StartClient()