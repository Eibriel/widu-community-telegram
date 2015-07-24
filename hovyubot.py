#!/bin/python3

import requests
from config import Config

last_update = 0
bot_token = Config.bot_token
server_url = Config.server_url

while 1:
    r = requests.get('https://api.telegram.org/bot{0}/getUpdates?timeout=30&offset={1}'.format(bot_token, last_update))
    r_json = r.json()
    #print (r_json)
    for result in r_json['result']:
        msg = ''
        if result['update_id'] >= last_update:
            last_update = result['update_id'] + 1
        chat_id = result['message']['chat']['id']
        if 'location' in result['message']:
            longitude = result['message']['location']['longitude']
            latitude = result['message']['location']['latitude']
            r = requests.get('{0}/stores?product=&activity=&latitude={1}&longitude={2}&page=1'.format(server_url, latitude, longitude))
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
        if 'text' in result['message']:
            if result['message']['text']:
                msg = 'Hola! Si me envías tu hubicación te puedo decir que comercios verdes hay por tu zona.\n Si quieres sumar un comercio o necesitas ayuda te invito a unirte a mi grupo:\nhttps://telegram.me/joinchat/0338811e00225f1561463d99065a12d7'
        r = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'.format(bot_token, chat_id, msg))
