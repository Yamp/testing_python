import configparser

from tools.db import Db

config = configparser.ConfigParser()
config.read(r'D:\Projects\Python\testing_python\setup.conf')

def getDbase():
    return config['dbase']['db']

def connQuantity():
    return int(config['dbase']['connections'])

def getPostgresParams():
    p = config['Postgresql']
    return Db.Postgres(p['host'], p['dbname'], p['user'], p['password'])

def getSqliteParams():
    return Db.Sqlite(config['Sqlite']['database'])

