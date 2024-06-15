import requests
import json
import db

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
    secret_key = response["secret_key"]
    device_name = db.get_device_name_by_secret_key(secret_key)
    return f'*From:* **{device_name}**\n*Message type:* {response["message_type"]}\n*Text:* {response["text"]}\n'


def get_server_status():
    try:
        url = config['monitor_url']
        response = requests.get(f"{url}/server")
        response.raise_for_status()
        return response.json().get('status', 'Unknown')
    except Exception as e:
        return f'Error: {str(e)}'


def get_db_status():
    try:
        url = config['monitor_url']
        response = requests.get(f"{url}/mongodb")
        response.raise_for_status()
        return response.json().get('status', 'Unknown')
    except Exception as e:
        return f'Error: {str(e)}'


def get_mobile_status(secret_keys):
    try:
        url = config['monitor_url']
        auth_key = config['authKey']
        response = requests.post(
            f"{url}/mobile/status",
            cookies={'__Secure-Auth-Token': auth_key},
            json={"secret_keys": secret_keys}
        )
        response.raise_for_status()
        mobile_status = response.json()
        # Remove last_updated from each key's status
        for key, value in mobile_status.items():
            mobile_status[key] = value['status']
        return mobile_status
    except Exception as e:
        return f'Error: {str(e)}'
