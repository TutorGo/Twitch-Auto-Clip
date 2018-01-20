import unittest
import socket
from time import sleep

from Setting import CHANNEL, HOST, PORT, twitch_token, NICK, twitch_client_id, twitch_secret, \
                    kakao_client_id, kakao_secret
from getaccesstoken import TokenHandler
from twitchcreateclip import get_channel_id, create_clip
from kakaotalksendmessage import send_clip_url
def loading_complete_check(line):
    """
    chat 들어 왔는지 확인
    """
    # 채팅방에 정상적으로 들어가게 되면 문자열에 End of /NAMES list 문자열 출력
    if "End of /NAMES list" in line:
        return False
    else:
        return True


def join_chat_room(socket):
    loading = True
    while loading:
        response = socket.recv(1024).decode("utf-8")
        loading = loading_complete_check(response)
    return loading


def open_socket():
    '''
    twitch 채팅 irc에 연결하기 위한 소켓 생성
    :return:
    '''

    # 소켓 생성
    s = socket.socket()
    # 호스트와 포트를 지정해서 연결
    s.connect((HOST, PORT))
    # PASS는 트위치 OAuth token https://twitchapps.com/tmi/ 발급 가능하다
    s.send("PASS {}\r\n".format(twitch_token).encode("utf-8"))
    # bot의 닉네인을 설정 한다는데 왜 나는 안될까.. 그냥 나의 닉네임이 나온다
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    # JOIN은 CHANNEL 들어가고 싶은 채널에 들어감
    s.send("JOIN {}\r\n".format(CHANNEL).encode("utf-8"))

    return s


class TestTwitchAutoClip(unittest.TestCase):

    def test_joinchatroom(self):
        s = open_socket()
        join_check = join_chat_room(s)
        self.assertEqual(False, join_check)

    def test_get_channel_id(self):
        _, status_code = get_channel_id(CHANNEL)
        self.assertEqual(status_code, 200)

    def test_send_clip_url(self):
        sleep(2)
        kakao_access_token, token_status_code = TokenHandler(kakao_client_id, kakao_secret).get_access_token(type='k')
        status_code = send_clip_url(kakao_access_token, 'IncredulousPerfectJamOSsloth')
        self.assertEqual(status_code, 200)
        self.assertEqual(token_status_code, 200)

    def test_create_clip(self):
        sleep(2)
        twitch_access_token, token_status_code = TokenHandler(twitch_client_id, twitch_secret).get_access_token()
        channel_id, _ = get_channel_id('woowakgood')
        _, status_code = create_clip(twitch_access_token, channel_id)
        self.assertEqual(token_status_code, 200 )
        self.assertEqual(status_code, 202)






