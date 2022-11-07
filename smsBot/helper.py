import requests
import json

def check_secret_key(uuid,secret_key):
    cookies = {'__Secure-Auth-Token': secret_key}
    url = 'http://127.0.0.1:80/assign-key?uuid='+uuid
    print(url)
    response = requests.post(url,cookies=cookies)
    if response.ok:
        return True
    else:
        return False

def get_sms():
    url = 'http://127.0.0.1:80/get-sms'
    response = requests.get(url)
    if not response.ok:
        return ''
    result = list(json.loads(response.text))
    return result

def get_message_from_response(response):
    m = f'*Message type:* {response["message_type"]}\n*Text:* {response["text"]}\n';
    return m;

def revoke(uuid):
    url = 'http://127.0.0.1:80/revoke?uuid='+uuid
    response = requests.post(url)
    return response.ok