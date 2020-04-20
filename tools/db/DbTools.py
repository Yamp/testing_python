from typing import *
from jinjasql import JinjaSql
import pandas as pd
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


def executeCommand(sql: str, connection=None, is_commit=True):
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
        print(line.getInt(0), line.getDate("f_date_doc"), line.getString('f_num_doc'), line.getBoolean("f_is_ready"),
              line.getString("sclad_name"))

    sql = "select f_cod, f_name from spr_scl"
    lines = getLines(sql, params)
    for line in lines:
        print(line.getInt(0), line.getString(1))

    sql = "select f_cod, f_name from spr_scl where f_id = 1"
    line = getLine(sql, params)
    print(line.getInt(0), line.getString(1))

    sql = "select f_name from spr_scl where f_id = 1"
    print(getString(sql))

    sql = "select max(f_date_doc) from docs"
    print(getDate(sql))

    sql = "select avg(f_id) from docs"
    print(getFloat(sql))

    # try:
    #     data = {"f_num_doc": 'Б3', "f_date_doc": RusDate.presentDate(), "f_sclad": 3, "f_is_ready": True}
    #     sql = SqlTools.sqlForInsert(data, "docs")
    #     executeCommand(sql)
    # except Exception as e:
    #     print(str(e))
