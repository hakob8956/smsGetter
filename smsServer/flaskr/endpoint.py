from flaskr.main import app
from flaskr.db import Db
from flask import Response, jsonify, request
from flaskr.helper import *


@app.route('/health', methods=['GET'])
def hello():
    # TODO: add db,service,bot checking
    return 'Working'


@app.route('/add-sms', methods=['POST'])
def add_sms():
    secret_key = request.cookies.get('__Secure-Secret-Key')
    auth_key = request.cookies.get('__Secure-Auth-Token')
    isChecked = validateAuthTgKey(auth_key)
    if (not isChecked):
        return Response('', status=403, mimetype='application/json')

    if (secret_key and not is_valid_uuid(secret_key)):
        return Response("", status=400, mimetype='application/json')

    if (not validateSMSRequest(request.json)):
        return Response("", status=400, mimetype='application/json')

    try:
        user = request.json[0]
        db = Db()
        db.insert_user(user, secret_key)
        return Response("", status=201, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("", status=500, mimetype='application/json')


@app.route('/get-sms', methods=['GET'])
def get_sms():
    try:
        auth_key = request.cookies.get('__Tg-Auth-Token')
        isChecked = validateAuthTgKey(auth_key)
        if (isChecked):
            db = Db()
            result = db.get_sms_assigned_bot()
            response = jsonify(result)
            return response
        return Response('', status=403, mimetype='application/json')

    except Exception as e:
        print(e)
        return Response("", status=500, mimetype='application/json')
