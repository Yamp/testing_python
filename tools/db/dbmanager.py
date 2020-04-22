import sqlite3
import psycopg2

import config
from tools.exceptions import NotFoundException


def _create_connection():
    dbase = config.dbase()
    if dbase == 'Postgresql':
        p = config.postgres_params()
        return psycopg2.connect(dbname=p.dbname, user=p.user,
                                password=p.password, host=p.host)
    elif dbase == 'Sqlite':
        return sqlite3.connect(config.sqlite_params().database)
    raise NotFoundException('unknown database')


conn_with_mark_busy_list = []
for i in range(config.conn_quantity()):
    conn_with_mark_busy_list.append([_create_connection(), False])


def get_connection():
    try:
        c = list(filter(lambda c: not c[1], conn_with_mark_busy_list))[0]
        c[1] = True
        return c[0]
    except:
        raise NotFoundException('All connections is using')


def free_connection(conn):
    conn = list(filter(lambda c: c[0] == conn, conn_with_mark_busy_list))[0]
    conn[1] = False


class DbConnection:
    def __init__(self) -> None:
        self.conn = get_connection()

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        free_connection(self.conn)
        return isinstance(value, TypeError)

class DbCursor:
    def __init__(self, connection):
        self.con = connection

    def __enter__(self):
        self.cursor = self.con.cursor()
        return self.cursor

    def __exit__(self, typ, value, traceback):
        self.cursor.close()

if __name__ == '__main__':
    print('dbase', config.dbase())
    print('conn_quantity =', config.conn_quantity())
    print(config.postgres_params())
    print(config.sqlite_params())

    with DbConnection() as conn, DbCursor(conn) as cursor:
        sql = 'SELECT f_num_doc, f_date_doc FROM docs order by 2 limit 10'
        cursor.execute(sql)
        records = cursor.fetchall()

        colnames = [desc[0] for desc in cursor.description]

        dbLines = [{colnames[0]: r[0], colnames[1]: r[1]} for r in records]
        for dbLine in dbLines:
            print(f'f_num_doc: {dbLine["f_num_doc"]} , \tf_date_doc: {dbLine["f_date_doc"]}' )

