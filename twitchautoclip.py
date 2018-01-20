import re
import socket
from time import sleep

from Setting import CHANNEL, HOST, PORT, twitch_token, NICK, RATE, twitch_client_id, twitch_secret, kakao_client_id, \
                    kakao_secret
from twitchcreateclip import get_channel_id, create_clip
from getaccesstoken import TokenHandler
from kakaotalksendmessage import send_clip_url


class TwitchAutoClip:
    def __init__(self, token, NICK, CHANNEL):
        self.PASS = token
        self.CHANNEL = '#' + CHANNEL
        self.NICK = NICK
        s = self.open_socket()
        self.join_chat_room(s)
        self.channel_id, _ = get_channel_id(CHANNEL)
        self.twitch_access_token, _ = TokenHandler(twitch_client_id, twitch_secret).get_access_token(type='t')
        sleep(2)
        self.kakao_access_token, _ = TokenHandler(kakao_client_id, kakao_secret).get_access_token(type='k')
        self.chat_count = 0
        self.clip_count = 0
        p = re.compile(r'#\w+\s:([ㄱ-ㅣ가-힣|\s|\W|\d]+)')
        while True:
            response = s.recv(1024).decode("utf-8")
            # twitch 서버에서 주기 적으로 봇이 살아 있나 PING을 보내기 떄문에 답을 해줘야 연결이 유지 가능함
            if response == "PING :tmi.twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                m = p.search(response)
                if m == None:
                    continue
                message = m.group(1)
                print(message)
                self.chat_count, self.clip_count = self.check_create_clip(self.chat_count, self.clip_count, message)
            # RATE = 20/30 으로 트위치에서 일반 유저는 30초에 20개의 메시지를 보낼 수 있기 때문에 설정
            sleep(1 / RATE)

    def loading_complete_check(self, line):
        """
        chat 들어 왔는지 확인
        """
        # 채팅방에 정상적으로 들어가게 되면 문자열에 End of /NAMES list 문자열 출력
        if "End of /NAMES list" in line:
            return False
        else:
            return True

    def join_chat_room(self, socket):
        loading = True
        while loading:
            response = socket.recv(1024).decode("utf-8")
            loading = self.loading_complete_check(response)
            print(response)

    def open_socket(self):
        '''
        twitch 채팅 irc에 연결하기 위한 소켓 생성
        :return:
        '''

        # 소켓 생성
        s = socket.socket()
        # 호스트와 포트를 지정해서 연결
        s.connect((HOST, PORT))
        # PASS는 트위치 OAuth token https://twitchapps.com/tmi/ 발급 가능하다
        s.send("PASS {}\r\n".format(self.PASS).encode("utf-8"))
        # bot의 닉네인을 설정 한다는데 왜 나는 안될까.. 그냥 나의 닉네임이 나온다
        s.send("NICK {}\r\n".format(self.NICK).encode("utf-8"))
        # JOIN은 CHANNEL 들어가고 싶은 채널에 들어감
        s.send("JOIN {}\r\n".format(self.CHANNEL).encode("utf-8"))

        return s

    def check_create_clip(self, chat_count, clip_count, message):
        if "ㅋㅋㅋ" in message:
            clip_count += 1
        elif clip_count >= 5:
            clip_id, _ = create_clip(self.twitch_access_token, self.channel_id)
            send_clip_url(self.kakao_access_token, clip_id)
            clip_count = 0
        elif chat_count >= 10:
            chat_count = 0
        chat_count += 1
        return chat_count, clip_count


TwitchAutoClip(twitch_token, NICK, CHANNEL)
