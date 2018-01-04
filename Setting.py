import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TWITCH_DIR = os.path.join(BASE_DIR, 'setting_twitch.json')

twitch = json.loads(open(TWITCH_DIR).read())

client_id = twitch['twitch']['client_id']
token = twitch['twitch']['token']

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "whatgsh"
CHANNEL = "www0606"
RATE = (20/30)