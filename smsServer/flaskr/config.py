import configparser


class Config:
    config = configparser.ConfigParser()
    config.read('../config.ini')
    connectionString = config['DEFAULT']['ConnectionStringMongoDb']
    authTgKey = config['DEFAULT']['AuthTgKey']
