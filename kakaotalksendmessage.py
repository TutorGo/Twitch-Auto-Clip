import requests
import json


def send_clip_url(access_token, clip_id):
    '''
    카카오톡 메시지 템플릿 v2에서 양식을 만들고 추가적으로 파라미터를 보내고 싶으면 템플릿에서 ${key} 방법으로 선언 합니다.
    그후 추가적인 인자는 파라미터에 template_args: json.dump({'key': value}) 보내면 됩니다.
    '''
    header = {'Authorization': 'Bearer ' + access_token}
    url = "https://kapi.kakao.com/v2/api/talk/memo/send"
    param = {'template_id': 7738, 'template_args': json.dumps({'clip_id': clip_id})}
    r = requests.post(url, params=param, headers=header)
    status_code = r.status_code

    return status_code