from ast import Try
from crypt import methods
from urllib import response
from flaskr.main import app
from flaskr.db import Db
from flask import Response, jsonify, request
from flaskr.helper import *



@app.route('/health',methods=['GET'])
def hello():
    #TODO: add db,service,bot checking
    return 'Working'


@app.route('/add-sms', methods=['POST'])
def add_sms():
    secret_key = request.cookies.get('__Secure-Auth-Token')
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


def check_secret_key_is_exists(secret_key):
    if secret_key and not is_valid_uuid(secret_key):
        return False
    db = Db()
    return db.check_secret_key(secret_key)


@app.route('/assign-key', methods=['POST'])
def assign_bot():
    uuid = request.args.get('uuid')
    secret_key = request.cookies.get('__Secure-Auth-Token')
    isChecked = check_secret_key_is_exists(secret_key)
    try:
        if isChecked:
            db = Db()
            db.assign_bot_to_user(uuid, secret_key)
            return Response('', status=201, mimetype='application/json')
        return Response('', status=403, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("", status=500, mimetype='application/json')


@app.route('/get-sms', methods=['GET'])
def get_sms():
    try:
        db = Db()
        result = db.get_sms_assigned_bot()
        response = jsonify(result)
        return response
    except Exception as e:
        print(e)
        return Response("", status=500, mimetype='application/json')


@app.route('/revoke', methods=['POST'])
def revoke():
    uuid = request.args.get('uuid')
    if not uuid:
        return Response("", status=400, mimetype='application/json')
    try:
        db = Db()
        db.revoke(uuid)
        return Response('', status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("", status=500, mimetype='application/json')
