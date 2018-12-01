import requests
import json
import random
from basic import get_products


access = 'access token'
id = 173111055


def get_longpoll():
    r = requests.get('https://api.vk.com/method/groups.getLongPollServer', params={'group_id': id, 'v': '8.86', 'access_token': access})

    return r.text


def check_longpoll(key, server, ts):
    r = requests.get(server.replace("\\", ""), params={'act': 'a_check','key': key, 'ts': ts, 'wait': 25})

    return r.text

first = eval(get_longpoll())
ts = first['response']['ts']
server = first['response']['server']
key = first['response']['key']

print(ts, server, key)

while True:
    check = json.loads(check_longpoll(key, server, ts))

    if 'failed' in check:
        if check['failed'] == 1:
            ts = check['ts']
        else:
            first = eval(get_longpoll())
            ts = first['response']['ts']
            server = first['response']['server']
            key = first['response']['key']

        continue
    ts = check['ts']

    for update in check['updates']:
        if update['type'] == 'message_new' and "хочу" in update['object']['text']:
            pr = get_products(update['object']['text'][5:])
            if pr == 'no': 
                r = requests.get('https://api.vk.com/method/messages.send', params={'user_id': update['object']['from_id'],
                                                                                'v': '8.86', 
                                                                                'access_token': access,
                                                                                'random_id': int(update['object']['from_id'])+int(update['object']['date'])+random.randint(0,100000000),
                                                                                'message': "nichego",
                                                                                'peer_id': update['object']['from_id']})
                continue

            message = "Товаров найдено: " + str(len(pr)) + "\n"

            for p in pr:
                """
                photo = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer', params={'peer_id': update['object']['from_id'],
                                                                                                        'access_token': access,
                                                                                                        'v': '8.86'})
                ph = requests.get(p.photo)
                photo = eval(requests.post(eval(photo.text.replace("\\", ""))['response']['upload_url'], files={'file':ph.content}).text)
                photo = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto', params={
                                                                                                    'photo':photo['photo'],
                                                                                                    'server':photo['server'],
                                                                                                    'hash':photo['hash'],
                                                                                                    'access_token': access,
                                                                                                        'v': '8.86'})
                """
                p_message = "Название: " + p.name + "\nЦена: " + p.cost 
                if p.stars:
                    p_message += "\nРейтинг: " + str(p.stars) 
                p_message += "\nСсылка: " + p.url + "\n"
                
                requests.get('https://api.vk.com/method/messages.send', params={'user_id': update['object']['from_id'],
                                                                                'v': '8.86', 
                                                                                'access_token': access,
                                                                                'random_id': int(update['object']['from_id'])+int(update['object']['date'])+random.randint(0,100000000),
                                                                                'message': p_message,
                                                                                'peer_id': update['object']['from_id'],
                                                                                #'attachment':'photo'+str(eval(photo.text)['owner_id'])+"_"+str(eval(photo.text)['id'])
                                                                                })

            message += "Больше товаров из Индии : https://deldelhi.ru \n\n"

            r = requests.get('https://api.vk.com/method/messages.send', params={'user_id': update['object']['from_id'],
                                                                                'v': '8.86', 
                                                                                'access_token': access,
                                                                                'random_id': int(update['object']['from_id'])+int(update['object']['date']),
                                                                                'message': message,
                                                                                'peer_id': update['object']['from_id']})
            




    print(check)
