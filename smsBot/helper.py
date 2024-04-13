import requests
import json

with open('config.json') as config_file:
    config = json.load(config_file)


def check_secret_key(uuid, secret_key):
    cookies = {'__Secure-Auth-Token': secret_key}
    url = f"{config['server_url']}/assign-key?uuid={uuid}"
    print(url)
    response = requests.post(url, cookies=cookies)
    return response.ok


def get_sms():
    cookies = {'__Tg-Auth-Token': config['authKey']}
    url = f"{config['server_url']}/get-sms"
    response = requests.get(url, cookies=cookies)
    if not response.ok:
        return ''
    return list(json.loads(response.text))


def get_message_from_response(response):
    return f'*Message type:* {response["message_type"]}\n*Text:* {response["text"]}\n'

