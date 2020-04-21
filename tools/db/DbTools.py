from typing import *

import pandas as pd
from jinjasql import JinjaSql

from tools.RusDate import RusDate
from tools.db import SqlTools
from tools.db.DbManager import DbConnection, DbCursor
from tools.exceptions import NotFoundException


class DbLine:
    def __init__(self, frameLine) -> None:
        self.line = frameLine

    def getDate(self, key) -> RusDate:
        return RusDate(self.line[key])

    def getString(self, key) -> str:
        return self.line[key]

    def getBoolean(self, key) -> bool:
        return self.line[key] != 0

    def getInt(self, key) -> int:
        return int(round(self.line[key]))

    def getFloat(self, key) -> float:
        return self.line[key]


def getFrame(sql: str, connection=None, params: Dict = None):
    """
    params = {
       'sclad': 3,
       'date_doc': RusDate('17/03/2020').d,
       'num_doc_template': '%Б%',
       'ids': (1,2,3,4,5,6,7),
       'is_ready': 1
    }
    sql = ...
    select docs.f_id, docs.f_num_doc, docs.f_date_doc, ss.f_name sclad_name, docs.f_is_ready
    from docs
             inner join spr_scl ss on docs.f_sclad = ss.f_cod
    where docs.f_date_doc >= {{ date_doc }}
      and docs.f_sclad = {{ sclad }} and docs.f_num_doc like {{num_doc_template}}
      and docs.f_id in {{ids | inclause}}
      and docs.f_is_ready = {{is_ready}}
    ...

    try:
        from jinjasql import JinjaSql
    
        j = JinjaSql(param_style='pyformat')
        query, bind_params = j.prepare_query(sql:str, params)
    
        print(query)
        print(bind_params)
    
        import pandas as pd
    
        with DbConnection() as conn:
            frm = pd.read_sql(query, conn, params=bind_params)
            keys = list(frm.keys())
    
            for item in keys:
                print(item, end=' ')
            print()
    
            for i in range(len(frm.values)):
                for key in keys:
                    print(frm.iloc[i][key], end=' ')
                print()
    except Exception as e:
        print(str(e))
    """
    j = JinjaSql(param_style='pyformat')
    if params is None:
        params = {}
    query, bind_params = j.prepare_query(sql, params)

    if connection is None:
        with DbConnection() as conn:
            return pd.read_sql(query, conn, params=bind_params)
    else:
        return pd.read_sql(query, connection, params=bind_params)


def getLines(sql: str, params: Dict = None, connection=None) -> List[DbLine]:
    frm = getFrame(sql, connection, params)
    return [DbLine(frm.iloc[i]) for i in range(len(frm.values))]


def getLine(sql: str, params: Dict = None, connection=None) -> DbLine:
    try:
        return getLines(sql, params, connection)[0]
    except IndexError:
        raise NotFoundException()


def getDate(sql: str, params: Dict = None, connection=None) -> RusDate:
    return getLine(sql, params, connection).getDate(0)


def getDates(sql: str, params: Dict = None, connection=None) -> List[RusDate]:
    frm, key = _getLineData(sql, params, connection)
    return [RusDate(value) for value in frm[key]]


def getString(sql: str, params: Dict = None, connection=None) -> str:
    return getLine(sql, params, connection).getString(0)


def getStrings(sql: str, params: Dict = None, connection=None) -> List[str]:
    frm, key = _getLineData(sql, params, connection)
    return frm[key]


def getBoolean(sql: str, params: Dict = None, connection=None) -> bool:
    return getLine(sql, params, connection).getBoolean(0)


def getBooleans(sql: str, params: Dict = None, connection=None) -> List[bool]:
    frm, key = _getLineData(sql, params, connection)
    return [value != 0 for value in frm[key]]


def getInt(sql: str, params: Dict = None, connection=None) -> int:
    return getLine(sql, params, connection).getInt(0)


def getInts(sql: str, params: Dict = None, connection=None) -> List[int]:
    frm, key = _getLineData(sql, params, connection)
    return [round(value) for value in frm[key]]


def getFloat(sql: str, params: Dict = None, connection=None) -> float:
    return getLine(sql, params, connection).getFloat(0)


def getFloats(sql: str, params: Dict = None, connection=None) -> List[float]:
    frm, key = _getLineData(sql, params, connection)
    return frm[key]


def _getLineData(sql, params, connection):
    frm = getFrame(sql, connection, params)
    key = frm.keys()[0]
    return frm, key


def executeCommand(sql: str, params=None, connection=None, is_commit=True):
    if connection is None:
        with DbConnection() as conn, DbCursor(conn) as cursor:
            _executeCommand(sql, params, conn, cursor, is_commit)
    else:
        with DbCursor(connection) as cursor:
            _executeCommand(sql, params, connection, cursor, is_commit)


def insert(table: str, fieldsWithValues: dict, connection=None, is_commit=True, is_next_id_by_hand: bool = False):
    """
    Добавить запись в таблицу
    :param table:
    :param fieldsWithValues:
    :param connection:
    :param is_commit:
    :param is_next_id_by_hand: если True, можно получить id таблицы для дальнейшего использования
    :return: id добавленой записи, или -1, если is_next_id_by_hand = False
    """
    next_id = -1
    if is_next_id_by_hand:
        seq_name = f'seq_{table}_f_id'
        sql = f"select nextval('{seq_name}')"
        next_id = getInt(sql, connection=connection)
        fieldsWithValues['f_id'] = next_id
    sql, params = SqlTools.sqlWithValuesForInsert(table, fieldsWithValues)
    executeCommand(sql, params, connection, is_commit)
    return next_id


def update(table: str, fieldsWithValues: dict, where: Any = '', connection=None, is_commit=True):
    """Обновить запись в таблице
       where может быть выражением типа 'f_num_doc = 34454',
       а может быть целым числом. Тогда преобразуется в f_id = 10
    """
    sql, params = SqlTools.sqlWithValuesForUpdate(table, fieldsWithValues, where)
    executeCommand(sql, params, connection, is_commit)


def _executeCommand(sql, params, conn, cursor, isCommit):
    if params is None:
        params = ()
    try:
        cursor.execute(sql, params)
    except:
        if isCommit:
            conn.rollback()
        raise
    else:
        if isCommit:
            conn.commit()


if __name__ == '__main__':
    try:
        params = {
            'sclad': 3,
            'date_doc': RusDate('17/03/2020').forSql(),
            'num_doc_template': '%Б%',
            'ids': (1, 2, 3, 4, 5, 6, 7),
            'is_ready': 1
        }
        sql = """
        select docs.f_id, docs.f_num_doc, docs.f_date_doc, ss.f_name sclad_name, docs.f_is_ready
        from docs
                 inner join spr_scl ss on docs.f_sclad = ss.f_cod
        where docs.f_date_doc >= {{ date_doc }}
          and docs.f_sclad = {{ sclad }} and docs.f_num_doc like {{num_doc_template}}
          and docs.f_id in {{ids | inclause}}
          and docs.f_is_ready = {{is_ready}}
        """

        lines = getLines(sql, params)
        for line in lines:
            print(line.getInt(0), line.getDate("f_date_doc"), line.getString('f_num_doc'),
                  line.getBoolean("f_is_ready"),
                  line.getString("sclad_name"))

        lines = getLines("select f_cod, f_name from spr_scl")
        for line in lines:
            print(line.getInt(0), line.getString(1))

        line = getLine("select f_cod, f_name from spr_scl where f_id = 1")
        print(line.getInt(0), line.getString(1))

        with DbConnection() as conn:
            print(getBoolean("select f_is_ready from docs where f_id = {{id}}", {'id': 2}, conn))
            print(getString("select f_name from spr_scl where f_id = {{id}}", {'id': 1}, conn))
            print(getDate("select max(f_date_doc) from docs", connection=conn))
            print(getFloat("select avg(f_id) from docs", connection=conn))
            ids = getFrame("select f_id, f_num_doc from docs", connection=conn)['f_id']
            print(ids.sum(), ids.min(), ids.max())
            frm = getFrame("select f_id, f_num_doc, f_sclad from docs", connection=conn)
            print(frm.eval('x = f_id + 100'))
            print(frm.groupby(['f_sclad']).max())

        ################################################################
        # update and insert
        fields = {
            'f_num_doc': 'Б14',
            'f_date_doc': RusDate.presentDate(),
            'f_sclad': 1,
            'f_is_ready': 0
        }
        insert('docs', fields)

        fields = {
            'f_num_doc': 'Б15',
            'f_date_doc': RusDate.presentDate(),
            'f_sclad': 1,
            'f_is_ready': 0
        }
        id = insert('docs', fields, is_next_id_by_hand=True)
        # Для последующего использования
        print(id)

        fields = {
            'f_date_doc': RusDate.presentDate() - 100,
            'f_sclad': 2,
            'f_is_ready': 1
        }
        update('docs', fields, 11)
        id = 10
        update('docs', fields, f'f_id = {(id + 1)}')
    except Exception as e1:
        print(str(e1))
