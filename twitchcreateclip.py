# from Setting import token, CHANNEL, client_id
# import requests
#
# channel = CHANNEL
#
# url = 'https://api.twitch.tv/kraken/users?login=' + channel
# headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
# r = requests.get(url, headers=headers).json()
# print(r.headers)
# channel_id = r['users'][0]['_id']
# print(channel_id)
#
# url = "https://api.twitch.tv/helix/clips?broadcaster_id="+channel_id
# headers = {"Authorization": "Bearer " + token}
# data = {"broadcaster_id": channel_id}
# r = requests.post(url, headers=headers)
# print(r.url)
# print(r.headers)
# print(r)
#
# # url = "https://api.twitch.tv/helix/clips"
# # headers = {'Client-ID': client_id}
# # param = {'id': 'FragileGeniusSrirachaJebaited'}
# # r = requests.get(url, headers=headers, params=param).json()
# # print(r)
