import os
import json
import random
import requests

from bson import ObjectId
from config import Config
from pymongo import MongoClient
from board_hello import board_hello


class bot:
    #last_update = 0
    #infers = []

    bot_token = Config.bot_token
    server_url = Config.server_url

    def __init__ (self):
        mongo_ip = 'localhost'
        if 'MONGODOCKERCOMPOSE_DB_1_PORT_27017_TCP_ADDR' in os.environ:
            mongo_ip = os.environ['MONGODOCKERCOMPOSE_DB_1_PORT_27017_TCP_ADDR']
        client = MongoClient(mongo_ip)
        db = client.emonitor
        self.db_settings = db.hovyubot_settings
        self.db_users = db.hovyubot_users
        #self.db_chats = db.hovyubot_chats

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

    def get_last_update(self):
        settings = self.db_settings.find()
        if settings.count() == 0:
            settings = {
                'last_update': 0
            }
            self.db_settings.insert(settings)
            return 0
        else:
            #print (settings[0])
            return settings[0]['last_update']


    def set_last_update(self, number):
        settings = {
            'last_update': number
        }
        settings_db = self.db_settings.find()[0]
        if settings_db:
            self.db_settings.update({'_id': settings_db['_id']}, {'$set': settings})
            return True
        else:
            return False


    def get_infer(self, user_id):
        user_db = self.db_settings.find_one({'tid': user_id})
        if user_db:
            return user_db['infers']
        else:
            return False


    def set_infer(self, user_id, infer):
        if type(infer) != list:
            return False
        user_db = self.db_settings.find_one({'tid': user_id})
        if not user_db:
            self.db_settings.insert({'tid': user_id, 'infers': infer})
            return True
        infers = list(set(user_db['infers'] + infer))
        self.db_settings.update({'_id': user_db['_id']}, {'$set': {'infers': infers}})

    def bot_loop(self):
        while 1:
            last_update = self.get_last_update()
            if last_update != 0:
                last_update = last_update + 1
            r = self.send_to_bot('getUpdates?timeout=30&offset={0}'.format(last_update))
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

                if result['update_id'] >= self.get_last_update():
                    self.set_last_update (result['update_id'])
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
                        self.set_infer(result['message']['from']['id'], infer)
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
                            #self.infers = list(set(self.infers + infer))
                            self.set_infer(result['message']['from']['id'], infer)
                        infers = self.get_infer(result['message']['from']['id'])
                        if 'children' in child:
                            for second_child in child['children']:
                                for node in board_hello['nodes']:
                                    if node['name']==second_child:
                                        dont_show = False
                                        if 'if_not' in node:
                                            #print (node['if_not'])
                                            #print (self.infers)
                                            for not_ in node['if_not']:
                                                if not_ in infers:
                                                    dont_show = True
                                                    break
                                        show = False
                                        if 'if' in node:
                                            for yes in node['if']:
                                                if yes in infers:
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
