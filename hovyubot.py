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

    chats = {}

    emoji_oh = '😱'
    emoji_silent = '😁'

    def __init__ (self):
        mongo_ip = 'localhost'
        if 'MONGODOCKERCOMPOSE_DB_1_PORT_27017_TCP_ADDR' in os.environ:
            mongo_ip = os.environ['MONGODOCKERCOMPOSE_DB_1_PORT_27017_TCP_ADDR']
        client = MongoClient(mongo_ip)
        db = client.hovyubot
        self.db_settings = db.settings
        self.db_users = db.users
        #self.db_chats = db.hovyubot_chats

    def send_to_bot(self, access_point, data=None):
        try:
            r = requests.get('https://api.telegram.org/bot{0}/{1}'.format(self.bot_token, access_point), data=data, timeout=40)
        except requests.exceptions.ConnectionError:
            print ("Connection Error")
            return None
        return r

    def send_to_widu(self, access_point, data=None, params=None):
        try:
            r = requests.get('{0}/{1}'.format(self.server_url, access_point), data=data, params=params, timeout=40)
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
        user_db = self.db_users.find_one({'tid': user_id})
        if user_db:
            return user_db['infers']
        else:
            return []


    def set_infer(self, user_id, infer):
        if type(infer) != list:
            return False
        user_db = self.db_users.find_one({'tid': user_id})
        if not user_db:
            self.db_users.insert({'tid': user_id, 'infers': infer})
            return True
        infers = list(set(user_db['infers'] + infer))
        self.db_users.update({'_id': user_db['_id']}, {'$set': {'infers': infers}})


    def search_place(self, name):
        data = {
            'find_places': name
        }
        items = self.send_to_widu('places', params=data)
        #print (items)
        place_items = []
        if not items:
            items = []
        else:
            items = items.json()['_items']
        for item in items:
            full_name = item['name']
            city = item['is_in']['city']
            state = item['is_in']['state']
            country = item['is_in']['country']
            if city:
                full_name = "{0}, {1}".format(full_name, city)
            if state:
                full_name = "{0}, {1}".format(full_name, state)
            if country:
                full_name = "{0}, {1}".format(full_name, country)

            if not city and not state and not country:
                near_name = item['near_place']['name']
                near_city = item['near_place']['city']
                near_state = item['near_place']['state']
                near_country = item['near_place']['country']
                full_name = "{0} ({1}".format(full_name, near_name)
                if near_city:
                    full_name = "{0}, {1}".format(full_name, near_city)
                if near_state:
                    full_name = "{0}, {1}".format(full_name, near_state)
                if near_country:
                    full_name = "{0}, {1}".format(full_name, near_country)
                full_name = "{0})".format(full_name)

            osm_id = item['osm_id']
            latitude = item['location']['coordinates'][0]
            longitude = item['location']['coordinates'][1]

            place_items.append({'_id': item['_id'],
                                'name': item['name'],
                                'full_name': full_name,
                                'osm_id': osm_id,
                                'latitude': latitude,
                                'longitude': longitude})
        return place_items

    def search_product(self, name):
        data = {
            'find_products': name
        }
        items = self.send_to_widu('products', params=data)
        products_items = []
        if not items:
            items = []
        else:
            items = items.json()['_items']
        for item in items:
            products_items.append({'_id': item['_id'], 'name': item['name']})
        return products_items

    def get_stores(self, product='', longitude=None, latitude=None, place=None):
        if place:
            r = self.send_to_widu('stores?product=&activity=&place_id={0}&page=1'.format(place))
        else:
            r = self.send_to_widu('stores?product=&activity=&latitude={0}&longitude={1}&page=1'.format(latitude, longitude))

        stores = r.json()['_items']
        if len(stores) == 0:
            msg = '''Ahora no recuerdo ningún comercio verde por esa zona, pero si me llego a acordar te aviso! 😊'
Mientras tanto puede unirte al grupo https://telegram.me/joinchat/0338811e00225f1561463d99065a12d7 para debatir y dejar comentarios'''
        else:
            if len(stores) == 1:
                msg = 'Sé de un comercio verde por tu zona:\n'
            else:
                msg = 'Sé de {0} comercios verdes por tu zona 😃\n'.format(len(stores))
            for store in stores:
                name = store['name']
                description =  store['description']
                address = store['address']
                time_bike = ''
                if store['distance_klm'] != None:
                    distance_klm = store['distance_klm']
                    if distance_klm < 1:
                        time_bike = '{0} minutos a pie'.format(int(round(distance_klm*9)))
                    else:
                        time_bike = '{0} minutos en bicicleta'.format(int(round(180/distance_klm)))
                if address == '':
                    address = '(No recuerdo la dirección 😶, deberás preguntar en el barrio)'
                msg = '{0}"{1}"\n{2}\n{3}\n{4}\n\n'.format(msg, name, description, address, time_bike)
        return msg

    def bot_loop(self):
        while 1:
            # Send messages
            users_db = self.db_users.find()
            #for user in users_db:
            #    data = {
            #        'chat_id': user['tid'],
            #        'text': 'Buenos días!',
            #    }
            #    r = self.send_to_bot('sendMessage', data = data)


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

            # Detect acumulated messages
            chats = {}
            for result in r_json['result']:
                chat_id = result['message']['chat']['id']
                if chat_id not in chats:
                    chats[ chat_id ] = []
                chats[ chat_id ].append(result['message'])
                if result['update_id'] >= self.get_last_update():
                    self.set_last_update (result['update_id'])

            #print (chats)
            for chat in chats:
                msgs = []
                # Too much messages to handle?
                messages_count = len(chats[chat])
                if messages_count > 3:
                    msgs.append(['{0} Me distraje un momento y ya tengo {1} notificaciones!'.format(self.emoji_oh, messages_count)])
                    # Process only first message
                    chats[chat] = [chats[chat][0]]

                for message in chats[chat]:
                #for result in r_json['result']:
                    children = None
                    infer = None
                    if_not = None
                    keys = []

                    chat_id = message['chat']['id']

                    # Location:
                    if 'location' in message:
                        longitude = message['location']['longitude']
                        latitude = message['location']['latitude']
                        msg = self.get_stores(longitude=longitude, latitude=latitude)
                        msgs.append([msg])
                        if not chat_id in self.chats:
                            self.chats[chat_id] = {}
                        self.chats[chat_id]['longitude'] = longitude
                        self.chats[chat_id]['latitude'] = latitude
                        msgs.append(['Si quieres buscar un producto en particular escribe "producto" y el nombre del producto, por ejemplo "producto milanesa".'])

                    # Text
                    if 'text' in message:
                        text = message['text']
                        if text == '/start':
                            text = '¡Buen día!'
                        elif text[0] == '/':
                            text = text[1:]
                        elif text[0:9] == '@HovyuBot ':
                            text = text[10:]

                        # Action
                        action = True
                        try:
                            option = int(text)
                        except:
                            action = False
                        if action:
                            if chat_id in self.chats and option in self.chats[chat_id]['options']:
                                if self.chats[chat_id]['action'] == 'zone':
                                    place_id = self.chats[chat_id]['options'][option]
                                    self.chats[chat_id]['place'] = place_id
                                    msg = self.get_stores(place = place_id)
                                    msgs.append([msg])
                                    msgs.append(['Si quieres buscar un producto en particular escribe "producto" y el nombre del producto, por ejemplo "producto milanesa".'])
                                elif self.chats[chat_id]['action'] == 'product':
                                    #print (self.chats[chat_id])
                                    if 'place' in self.chats[chat_id] or 'longitude' in self.chats[chat_id]:
                                        product_id = self.chats[chat_id]['options'][option]
                                        place_id = self.chats[chat_id].get('place', '')
                                        longitude = self.chats[chat_id].get('longitude')
                                        latitude = self.chats[chat_id].get('latitude')
                                        msg = self.get_stores(product=product_id, place = place_id, longitude=longitude, latitude=latitude)
                                        msgs.append([msg])
                                    else:
                                        msgs.append(['No me indicaste donde quieres buscar'])
                                        msgs.append(['Envíame tu ubicación o escribe "zona" y el nombre de tu ciudad, por ejemplo "zona Bahía Blanca"'])
                            else:
                                msgs.append(['No conozco esa opción... {0}'.format(self.emoji_silent)])

                        # Zone
                        if text[0:5] == 'zona ':
                            text = text[5:]
                            places = self.search_place(text)
                            if len(places) > 0:
                                places_names = ''
                                place_number = 0
                                options = {}
                                for place in places:
                                    places_names = '{0}\n{1}. {2}'.format(places_names, place_number, place['full_name'])
                                    options[place_number] = place['_id']
                                    place_number += 1
                                if not chat_id in self.chats:
                                    self.chats[chat_id] = {}
                                self.chats[chat_id]['action'] = 'zone'
                                self.chats[chat_id]['options'] = options
                                msgs.append([places_names])
                                if len(places) == 1:
                                    msg = self.get_stores(place = places[0]['_id'])
                                    msgs.append([msg])
                                    msgs.append(['Si quieres buscar un producto en particular escribe "producto" y el nombre del producto, por ejemplo "producto milanesa".'])
                                else:
                                    msgs.append(['Escribe el número del lugar donde quieres que busque'])
                            else:
                                msgs.append(['No conozco ese lugar... ¿Está bien escrito?'])

                        # Product
                        if text[0:9] == 'producto ':
                            if chat_id in self.chats and ('place' in self.chats[chat_id] or ('latitude' in self.chats[chat_id])):
                                text = text[9:]
                                products = self.search_product(text)
                                if len(products) > 0:
                                    products_names = ''
                                    product_number = 0
                                    options = {}
                                    for product in products:
                                        products_names = '{0}\n{1}. {2}'.format(products_names, product_number, product['name'])
                                        options[product_number] = product['_id']
                                        product_number += 1
                                    if not chat_id in self.chats:
                                        self.chats[chat_id] = {}
                                    self.chats[chat_id]['action'] = 'product'
                                    self.chats[chat_id]['options'] = options
                                    msgs.append([products_names])
                                    if len(products) == 1:
                                        #msg = self.get_stores(place = places[0]['_id'])
                                        #msgs.append([msg])
                                        pass
                                    else:
                                        msgs.append(['Escribí el número del producto donde querés que busque'])
                                else:
                                    msgs.append(['No conozco ese producto... ¿Está bien escrito?'])
                            else:
                                msgs.append(['No me indicaste donde quieres buscar'])
                                msgs.append(['Envíame tu ubicación o escribe "zona" y el nombre de tu ciudad, por ejemplo "zona Bahía Blanca"'])

                        # Dialog
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
                            self.set_infer(message['from']['id'], infer)
                        #print (self.infers)
                        if children:
                            children_name = random.choice(children) # TODO No Random
                            for node in board_hello['nodes']:
                                if node['name']==children_name:
                                    child = node
                                    break
                            msgs = msgs + random.choice(child['text'])
                            if 'infer' in child:
                                infer = node['infer']
                                #self.infers = list(set(self.infers + infer))
                                self.set_infer(message['from']['id'], infer)
                            infers = self.get_infer(message['from']['id'])
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
    Bot.bot_loop()
    try:
        Bot.bot_loop()
    except KeyboardInterrupt:
        break
    except:
        print ('Exception')
