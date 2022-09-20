from threading import local
import requests
import json
import datetime
import telebot

file = open('credentials.json')
data = json.load(file)

bot = telebot.TeleBot(data['apiKeyTelebot'], parse_mode=None)


tex = """
Добрый день, everybody🌞

Актуальный курс криптовалют специально для
подписчиков канала CryptoBoat (https://t.me/cryptoSunGA):
"""

tex2 = """
Какую валюту со сводки убрать, какую добавить? Предложения в комменты:
"""

currencies = [
    'BTC',
    'ETH',
    'SOL',
    'DOT',
    'LTC'
]

res_text = ""

today_date = datetime.datetime.today().strftime ('%Y-%m-%d')

previous_date = datetime.datetime.today() - datetime.timedelta(days=1)
previous_date = previous_date.strftime ('%Y-%m-%d')

for cur in currencies:

    url = "https://rest-sandbox.coinapi.io/v1/exchangerate/{}/USD?apikey={}&time={}".format(cur, data['apiKeyCrypto'], today_date)
    url_prev = "https://rest-sandbox.coinapi.io/v1/exchangerate/{}/USD?apikey={}&time={}".format(cur, data['apiKeyCrypto'], previous_date)

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_prev = requests.request("GET", url_prev, headers=headers, data=payload)


    res = json.loads(response.text)
    res_prev = json.loads(response_prev.text)

    percent = int(res['rate']) / int(res_prev['rate']) * 100 - 100
    percent = round(percent, 2)
    percent = "+{}".format(percent) if percent > 0 else percent
    percent = "{}%".format(percent)

    res_text += "{} - {}({})\n".format(cur, round(res['rate'], 2), percent)


message = "{}\n{}{}\n".format(tex, res_text, tex2)


bot.send_message(data['channel'], message)

