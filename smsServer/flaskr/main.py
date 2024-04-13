import os
from flaskr.mongoflask import MongoJSONEncoder, ObjectIdConverter

from flask import Flask
from flaskr.config import Config;

app = Flask(__name__, instance_relative_config=False)
app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectid'] = ObjectIdConverter


from  flaskr.endpoint import *