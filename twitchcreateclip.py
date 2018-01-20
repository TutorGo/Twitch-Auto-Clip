from Setting import twitch_client_id
import requests



def get_channel_id(channel):
    """
    clip을 생성하기 위해서는 channel_id 가 필요함 그래서 channel_id를 구하기 위한 함수
    :param channel: twitch channel ex): https://www.twitch.tv/(hardbar12) << 채널
    :return:
    """
    GET_CLIENT_ID_URI = 'https://api.twitch.tv/kraken/users?login=' + channel
    headers = {'Client-ID': twitch_client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
    response = requests.get(GET_CLIENT_ID_URI, headers=headers).json()
    status_code = requests.get(GET_CLIENT_ID_URI, headers=headers).status_code
    channel_id = response['users'][0]['_id']

    return channel_id, status_code


def create_clip(access_token, channel_id):
    """

    clip 생성하는 함수
    :param channel_id:
    :return:
    """
    CREATE_CLIP_URI = "https://api.twitch.tv/helix/clips"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"broadcaster_id": channel_id}
    response = requests.post(CREATE_CLIP_URI, headers=headers, params=params)
    # 카카오톡 나에게 보내기를 사용할때 이미지 클릭시 clip으로 넘어가기 위해서 clip_id가 필요함
    print(response.json())
    clip_id = response.json()['data'][0]['id']
    status_code = response.status_code
    return clip_id, status_code
