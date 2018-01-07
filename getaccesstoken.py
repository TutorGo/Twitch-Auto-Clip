import re
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from webbrowser import open_new
from Setting import client_id, secret

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
        # twtuch code를 얻기 위한 uri
        GET_TWITCH_CODE_URI = ("https://api.twitch.tv/kraken/oauth2/" + 'authorize?client_id=' + client_id
                               + '&redirect_uri=' + REDIRECT_URL + '&response_type=code' + '&scope=clips:edit')
        # uri을 브라우저로 실행

        open_new(GET_TWITCH_CODE_URI)

        # lambda request, address, server: HTTPServerHandler 이 부분에서 request, address, server
        # HTTPServerHandler에 self._id, self._secret 넣기 위해 존재하는 것 이라고 보면 됌 request, address, server 에는
        # 아무것도 들어오지 않음
        httpServer = HTTPServer(('localhost', 8000), lambda request, address, server: \
            HTTPServerHandler(request, address, server, self._id, self._secret))

        # http 요청을 한 번만 받음
        httpServer.handle_request()

        return httpServer.access_token, httpServer.access_token_status_code
