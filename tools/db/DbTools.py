from tools.RusDate import RusDate
from tools.db import SqlTools
from tools.db.DbManager import DbConnection, DbCursor


def executeCommand(sql, connection=None, is_commit=True):
    if connection is None:
        with DbConnection() as conn, DbCursor(conn) as cursor:
            _executeCommand(conn, cursor, is_commit, sql)
    else:
        with DbCursor(connection) as cursor:
            _executeCommand(connection, cursor, is_commit, sql)


def _executeCommand(conn, cursor, isCommit, sql):
    try:
        cursor.execute(sql)
    except:
        if isCommit:
            conn.rollback()
        raise
    else:
        if isCommit:
            conn.commit()


if __name__ == '__main__':
    try:
        data = {"f_num_doc": 'Б3', "f_date_doc": RusDate.presentDate(), "f_sclad": 3, "f_is_ready": True}
        sql = SqlTools.sqlForInsert(data, "docs")
        executeCommand(sql)
    except Exception as e:
        print(str(e))

# import sqlite3
# conn = sqlite3.connect('dbase1')
# curs = conn.cursor()
#
# # tblcmd = 'create table people (name char(30), job char(10), pay int(4))'
# # curs.execute(tblcmd)
# curs.execute('insert into people values (?, ?, ?)', ('Bob', 'dev', 5000))
# curs.executemany('insert into people values (?, ?, ?)', [ ('Sue', 'mus', '70000'), ('Ann', 'mus', '60000')])
#
# rows = [['Tom', 'mgr', 100000],
# ['Kim', 'adm', 30000],
# ['pat', 'dev', 90000]]
# for row in rows:
#     curs.execute('insert into people values (? , ?, ?)', row)
#
# conn.commit()
#
# curs.execute('select * from people')
# print(curs.fetchall())
