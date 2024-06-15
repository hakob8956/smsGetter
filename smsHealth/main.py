from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta
from pymongo import MongoClient
import requests
import json
import time

app = Flask(__name__, instance_relative_config=False)

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Store the mobile status in a global dictionary (In a real-world application, consider using a database)
mobile_service_status = {}


def check_mongodb_status():
    mongo_url = config['SERVICES']['mongodb']
    try:
        print("Hakob", mongo_url)
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=1000)
        client.server_info()  # Trigger exception if MongoDB is not reachable
        return "online"
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return "offline"


def check_server_status():
    server_url = config['SERVICES']['server']
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            return "online"
        else:
            return "offline"
    except Exception as e:
        print(f"Server status error: {e}")
        return "offline"


def check_telegram_bot_status():
    token = config['TELEGRAM_BOT_TOKEN']
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json().get('ok'):
            return "online"
        else:
            return "offline"
    except Exception as e:
        print(f"Telegram bot status error: {e}")
        return "offline"


def validateAuthTgKey(auth_key):
    # Placeholder function for authentication validation logic
    # Implement the actual authentication logic here
    valid_keys = config['AUTH_KEY']
    return auth_key in valid_keys


@app.route('/mongodb', methods=['GET'])
def mongodb_health():
    status = check_mongodb_status()
    return jsonify({"status": status}), 200 if status == "online" else 500


@app.route('/server', methods=['GET'])
def server_health():
    status = check_server_status()
    print(status)
    return jsonify({"status": status}), 200 if status == "online" else 500


@app.route('/bot', methods=['GET'])
def bot_health():
    status = check_telegram_bot_status()
    return jsonify({"status": status}), 200 if status == "online" else 500


@app.route('/mobile', methods=['POST'])
def mobile_health_update():
    secret_key = request.cookies.get('__Secure-Secret-Key')
    auth_key = request.cookies.get('__Secure-Auth-Token')
    print(secret_key)
    print(auth_key)
    isChecked = validateAuthTgKey(auth_key)
    if not isChecked:
        return Response('', status=403, mimetype='application/json')
    try:
        global mobile_service_status
        mobile_service_status[secret_key] = {
            "status": "online",
            "last_updated": time.time()
        }
    except Exception as e:
        print(f"Telegram bot status error: {e}")
        return jsonify({"message": "Something went wrong"}), 415
    return jsonify({"message": "Mobile status updated"}), 200


@app.route('/mobile/status', methods=['POST'])
def get_mobile_health():
    auth_key = request.cookies.get('__Secure-Auth-Token')
    isChecked = validateAuthTgKey(auth_key)
    if not isChecked:
        return Response('', status=403, mimetype='application/json')

    data = request.json
    secret_keys = data.get("secret_keys", [])
    print("secret_key received ", secret_keys)
    print(mobile_service_status)
    result = {}

    current_time = datetime.now()
    six_minutes_ago = current_time - timedelta(minutes=6)

    for key in secret_keys:
        if key in mobile_service_status:
            last_updated_timestamp = mobile_service_status[key]['last_updated']
            last_updated = datetime.fromtimestamp(last_updated_timestamp)
            if last_updated < six_minutes_ago:
                result[key] = {
                    "status": "offline",
                    "last_updated": last_updated.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                result[key] = {
                    "status": mobile_service_status[key]['status'],
                    "last_updated": last_updated.strftime("%Y-%m-%d %H:%M:%S")
                }
        else:
            result[key] = {"message": "Status not found"}

    return jsonify(result), 200
