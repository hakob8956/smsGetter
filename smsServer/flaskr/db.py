from pymongo import MongoClient
from dateutil import parser

from flaskr.config import Config


class Db:
    def __init__(self):
        self.client = self.get_database()

    def get_database(self):
        CONNECTION_STRING = Config().connectionString
        try:
            client = MongoClient(CONNECTION_STRING)
        except Exception as e:
            print(e)
            print("Connection error")
            exit(1)

        return client['SMS_Getter']

    def insert_user(self, user, secret_key):
        user_data = list(self.find_user_by_secret_key(secret_key))
        # uuid = ''
        # if (len(user_data) > 0 and user_data[0].__contains__('uuid') and user_data[0]['uuid'] != ''):
        #     uuid = user_data[0]['uuid']
        new_user = {
            'secret_key': secret_key,
            'device_id': user['device_id'],
            'message_type': user['message_type'],
            'date_time': parser.parse(user['date_time']),
            'sms_date_time': parser.parse(user['sms_date_time']),
            'tel': user['tel'],
            'text': user['text'],
            'isReaded': False,
            # 'uuid': uuid
        }
        print(new_user)
        self.client['user'].insert_one(new_user)

    def find_user_by_secret_key(self, secret_key):
        return self.client['user'].find({'secret_key': secret_key})

    def check_secret_key(self, secret_key):
        return len(list(self.find_user_by_secret_key(secret_key))) > 0

    def assign_bot_to_user(self, uuid, secret_key):
        query = {'secret_key': secret_key}
        setQuery = {'$set': {'uuid': uuid}}
        self.client['user'].update_many(query, setQuery)

    def get_sms(self, uuid):
        result = list(self.client['user'].find(
            {'uuid': uuid, 'isReaded': False}))
        if len(result) > 0:
            query = {'uuid': uuid, 'isReaded': False}
            setQuery = {'$set': {'isReaded': True}}
            self.client['user'].update_many(query, setQuery)

        return result

    def get_sms_assigned_bot(self):
        try:
            result = list(self.client['user'].find(
                {'isReaded': False}))
            if len(result) > 0:
                query = {'isReaded': False}
                setQuery = {'$set': {'isReaded': True}}
                self.client['user'].update_many(query, setQuery)
                print(result)
                result = [{key: value for key, value in doc.items() if key != '_id'}
                          for doc in result]
        except Exception as e:
            print(e)
        return result

    def revoke(self, uuid):
        query = {'uuid': uuid}
        setQuery = {'$set': {'uuid': ''}}
        self.client['user'].update_many(query, setQuery)
