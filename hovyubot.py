#!/bin/python3

import json
import random
import requests
from config import Config

from board_hello import board_hello

class bot:
    last_update = 0
    bot_token = Config.bot_token
    server_url = Config.server_url

    last = ''

    infers = []

    def send_to_bot(self, access_point, data=None):
        try:
            r = requests.get('https://api.telegram.org/bot{0}/{1}'.format(self.bot_token, access_point), data=data)
        except requests.exceptions.ConnectionError:
            print ("Connection Error")
            return None
        return r

    def send_to_widu(self, access_point, data=None):
        try:
            r = requests.get('{0}/{1}'.format(self.server_url, access_point), data=data)
        except requests.exceptions.ConnectionError:
            print ("Connection Error")
            return None
        return r

    def bot_loop(self):
        while 1:
            r = self.send_to_bot('getUpdates?timeout=30&offset={0}'.format(self.last_update))
            if not r:
                continue
            r_json = r.json()
            #print (r_json)
            if not r_json['ok']:
                break
            for result in r_json['result']:
                msgs = []
                children = None
                infer = None
                if_not = None
                keys = []

                if result['update_id'] >= self.last_update:
                    self.last_update = result['update_id'] + 1
                chat_id = result['message']['chat']['id']

                # Location:
                if 'location' in result['message']:
                    longitude = result['message']['location']['longitude']
                    latitude = result['message']['location']['latitude']
                    r = self.send_to_widu('stores?product=&activity=&latitude={0}&longitude={1}&page=1'.format(latitude, longitude))
                    #print (r.text)
                    stores = r.json()['_items']
                    if len(stores) == 0:
                        msg = 'Ahora no recuerdo ningún comercio verde por esa zona, pero si me llego a acordar te aviso! 😊'
                    else:
                        if len(stores) == 1:
                            msg = 'Sé de un comercio verde por tu zona:\n'
                        else:
                            msg = 'Sé de {0} comercios verdes por tu zona 😃\n'.format(len(stores))
                        for store in stores:
                            name = store['name']
                            description =  store['description']
                            address = store['address']
                            distance_klm = store['distance_klm']
                            if distance_klm < 1:
                                time_bike = '{0} minutos a pie'.format(int(round(distance_klm*9)))
                            else:
                                time_bike = '{0} minutos en bicicleta'.format(int(round(180/distance_klm)))
                            if address == '':
                                address = '(No recuerdo la dirección 😶, deberás preguntar en el barrio)'
                            msg = '{0}"{1}"\n{2}\n{3}\n{4}\n\n'.format(msg, name, description, address, time_bike)
                    msgs = [msg]

                # Text
                if 'text' in result['message']:
                    text = result['message']['text']
                    if text == '/start':
                        text = '¡Buen día!'
                    elif text[0] == '/':
                        text = text[1:]
                    elif text[0:9] == '@HovyuBot ':
                        text = text[10:]
                    for node in board_hello['nodes']:
                        for node_text in node['text']:
                            if [text] == node_text:
                                if 'children' in node:
                                    children = node['children']
                                if 'infer' in node:
                                    infer = node['infer']
                                break
                        if children:
                            break
                    #print (infer)
                    if infer:
                        self.infers = list(set(self.infers + infer))
                    #print (self.infers)
                    if children:
                        children_name = random.choice(children) # TODO No Random
                        for node in board_hello['nodes']:
                            if node['name']==children_name:
                                child = node
                                break
                        msgs = random.choice(child['text'])
                        if 'infer' in child:
                            infer = node['infer']
                            self.infers = list(set(self.infers + infer))
                        if 'children' in child:
                            for second_child in child['children']:
                                for node in board_hello['nodes']:
                                    if node['name']==second_child:
                                        dont_show = False
                                        if 'if_not' in node:
                                            #print (node['if_not'])
                                            #print (self.infers)
                                            for not_ in node['if_not']:
                                                if not_ in self.infers:
                                                    dont_show = True
                                                    break
                                        show = False
                                        if 'if' in node:
                                            for yes in node['if']:
                                                if yes in self.infers:
                                                    show = True
                                                    break
                                        else:
                                            show = True
                                        #print (node['name'])
                                        #print ('SHOW {0}'.format(show))
                                        #print ('DONT SHOW {0}'.format(dont_show))
                                        if show and not dont_show:
                                            keys.append([random.choice(node['text'])[0]])
                                        break

                keyboard = {
                    "keyboard": keys,
                    "resize_keyboard": True
                }
                for  msg in msgs:
                    data = {
                        'chat_id': chat_id,
                        'action': 'typing'
                    }
                    r = self.send_to_bot('sendChatAction', data = data)
                    data = {
                        'chat_id': chat_id,
                        'text': msg,
                    }
                    #print (keys)
                    if len(keys)>0:
                        data['reply_markup'] = json.dumps(keyboard)
                    r = self.send_to_bot('sendMessage', data = data)

Bot = bot()

while 1:
    #Bot.bot_loop()
    try:
        Bot.bot_loop()
    except KeyboardInterrupt:
        break
    except:
        print ('Exception')
