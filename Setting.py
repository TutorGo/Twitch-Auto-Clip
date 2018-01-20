import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TWITCH_DIR = os.path.join(BASE_DIR, 'setting_twitch.json')
DRIVER_DIR = os.path.join(BASE_DIR, 'chromedriver')

app = json.loads(open(TWITCH_DIR).read())

twitch_client_id = app['twitch']['client_id']
twitch_secret = app['twitch']['secret']
twitch_token = app['twitch']['token']

kakao_client_id = app['kakao']['client_id']
kakao_secret = app['kakao']['secret']

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "gsh2448"
CHANNEL = "caroline9071"
RATE = (20/30)