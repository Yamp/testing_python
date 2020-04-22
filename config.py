import configparser

from tools.db import db

config = configparser.ConfigParser()
config.read(r'D:\Projects\Python\testing_python\setup.conf')


def dbase():
    return config['dbase']['db']


def conn_quantity():
    return int(config['dbase']['connections'])


def postgres_params():
    p = config['Postgresql']
    return db.Postgres(p['host'], p['dbname'], p['user'], p['password'])


def sqlite_params():
    return db.Sqlite(config['Sqlite']['database'])
