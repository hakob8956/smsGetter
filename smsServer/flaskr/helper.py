from uuid import UUID
from jsonschema import validate
from flaskr.config import Config

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string"
                },
                "message_type": {
                    "type": "string"
                },
                "date_time": {
                    "type": "string"
                },
                "sms_date_time": {
                    "type": "string"
                },
                "tel": {
                    "type": "string"
                },
                "text": {
                    "type": "string"
                }
            },
            "required": [
                "device_id",
                "message_type",
                "date_time",
                "sms_date_time",
                "tel",
                "text"
            ]
        }
    ]
}


def validateAuthTgKey(key):
    print(Config().authTgKey)
    return key == Config().authTgKey


def validateSMSRequest(body):
    try:
        validate(instance=body, schema=schema)
        return True
    except Exception as e:
        print(e)
        return False


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
