import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import requests

from Setting import client_id, secret, DRIVER_DIR

REDIRECT_URL = 'http://localhost:8000'


class HTTPServerHandler(BaseHTTPRequestHandler):
    """
    twitch Oauth 가 다시 돌아오는 HTTP server
    """

    def __init__(self, request, address, server, c_id, c_secret):
        self.app_id = c_id
        self.app_secret = c_secret
        super().__init__(request, address, server)

    def do_GET(self):
        """
        TokenHandler.get_access_token의 open_new(GET_TWITCH_CODE_URI)로 인해서 켜진 twtich login 뜨는데
        아이디 비밀번호를 입력하면 redirect_uri로 설정된 곳으로 요청이 오는데 그 요청에서 code를 받고 다시 twitch로 보내서
        access_token을 받음
        """
        # token정보를 받기 위한 uri
        GET_TWITCH_AUTH_URI = ('https://api.twitch.tv/kraken/oauth2/'
                               + 'token/?client_id=' + client_id + '&client_secret=' + secret
                               + '&grant_type=authorization_code' + '&redirect_uri=' + REDIRECT_URL
                               + '&code=')
        # 200 요청을 보냄
        self.send_response(200)
        # 특별한 헤더가 없으면 send_response뒤에는 end_headers 가 바로 붙어야함
        self.end_headers()

        # reidert 된 uri에서 code의 패턴
        # 여기서 잠깐! 왜 url이라고 안하고 uri라고 하는가? URL은 Uniform Resource Locator 자원의 위치를 가르키기 때문에
        # http://test.com/work/sample.pdf 으로 된 것이 URL이고 URI는 URI는 Uniform Resource Identifier 에
        # url로 실행되는 서비스는 uri라고 한다
        pattern = re.compile(r'code=(\w+)')

        # self.path(현재 uri)에서 code가 있을 때
        if 'code' in self.path:
            m = pattern.search(self.path)
            code = (m.group(1))
            url = GET_TWITCH_AUTH_URI + code
            # 이 부분에서 바로 access_token을 리턴 할 수 있지만 안하는 이유는 test code를 위한 것이다
            # access_token 받아올때 스테이터스 코드로 받아와서 test code에 적용 할 것 임
            r = requests.post(url)
            result_json = r.json()
            self.server.access_token_status_code = r.status_code
            self.server.access_token = result_json['access_token']

class TokenHandler:
    """
    Twitch token을 처리 하기 위한 클래스
    """

    def __init__(self, c_id, c_secret):
        """

        :param c_id: twitch client_id
        :param c_secret: twitch secret_id
        """
        self._id = c_id
        self._secret = c_secret

    def get_access_token(self):
        """
        토큰을 얻기 위한 함수
        """
        # twtuch code를 얻기 위한 uri scope=clips:edit 이 있어야 token에 클립을 생성할 수 있는 권한을 얻는다.
        GET_TWITCH_CODE_URI = ("https://api.twitch.tv/kraken/oauth2/" + 'authorize?client_id=' + client_id
                               + '&redirect_uri=' + REDIRECT_URL + '&response_type=code' + '&scope=clips:edit')
        # uri을 브라우저로 실행
        # 처음에는 open_new(GET_TWITCH_CODE_URI) 구현했지만 python의 webbrowser는 browser 닫히지 않아서 수동으로 직접
        # 닫아줘야 합니다. 두 번째 방법으로는 Popen 으로 실행시켜서 프로세스를 제거하는 방법입니다. 하지만 Popen으로 browser를 실행시키면
        # 실행시킨 browser는 다른 프로세스 입니다 즉 Popen의 프로세스를 종료시켜도 브라우저는 그대로 있습니다. 그래서 browser의
        # 프로세스 아이디를 kill 시키면 browser 꺼지는 게 아니라 그냥 연결만 끊어지고 browser 켜진 상태로 있습니다
        # 그래서 결국 selenium의 webdriver를 사용해야 했습니다

        # Chrome에 cromedriver의 결로를 설정 해줘야함
        # https://sites.google.com/a/chromium.org/chromedriver/downloads << 다운로드 경로
        browser = webdriver.Chrome(DRIVER_DIR)
        # url로 browser 실행
        browser.get(GET_TWITCH_CODE_URI)
        # browser 켠다고 browser 포커스가 옮겨지는 것이 아니라 알람 기능을 사용해야 했습니다
        # execute_script는 browser 에서 자바스크립트를 동작시키게 하는 함수 입니다.
        browser.execute_script("window.alert('')")
        # 알람을 자동으로 확인 합니다.
        Alert(browser).accept()

        # lambda request, address, server: HTTPServerHandler 이 부분에서 request, address, server
        # HTTPServerHandler에 self._id, self._secret 넣기 위해 존재하는 것 이라고 보면 됌 request, address, server 에는
        # 아무것도 들어오지 않음
        httpServer = HTTPServer(('localhost', 8000), lambda request, address, server: \
            HTTPServerHandler(request, address, server, self._id, self._secret))

        # http 요청을 한 번만 받음
        httpServer.handle_request()
        # check_call(['kill', '/F','/T','/PID', str(p.pid)])
        sleep(3)
        # 현재 띄워진 창을 자동으로 닫습니다. close는 chrome 자체를 종료시키는 것이고 quit는 창을 닫기만 하는 차이 입니다.
        browser.close()
        return httpServer.access_token, httpServer.access_token_status_code


