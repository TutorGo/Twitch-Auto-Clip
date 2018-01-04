import socket
from time import sleep

from Setting import CHANNEL, HOST, PORT, token, NICK, RATE


class TwitchAutoClip:
    def __init__(self, token, NICK, CHANNEL):
        self.PASS = token
        self.CHANNEL = '#' + CHANNEL
        self.NICK = NICK
        s = self.open_socket()
        self.join_chat_room(s)

        while True:
            response = s.recv(1024).decode("utf-8")
            # twitch 서버에서 주기 적으로 봇이 살아 있나 PING을 보내기 떄문에 답을 해줘야 연결이 유지 가능함
            if response == "PING :tmi.twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                print(response)
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
        s.send("PASS {}\r\n".format(token).encode("utf-8"))
        # bot의 닉네인을 설정 한다는데 왜 나는 안될까.. 그냥 나의 닉네임이 나온다
        s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
        # JOIN은 CHANNEL 들어가고 싶은 채널에 들어감
        s.send("JOIN {}\r\n".format(CHANNEL).encode("utf-8"))

        return s

TwitchAutoClip(token,NICK,CHANNEL)