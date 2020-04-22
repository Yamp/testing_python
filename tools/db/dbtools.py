from typing import *

import pandas as pd
from jinjasql import JinjaSql

from tools.rus_date import RusDate
from tools.db import sqltools
from tools.db.dbmanager import DbConnection, DbCursor
from tools.exceptions import NotFoundException


class DbLine:
    def __init__(self, frameLine) -> None:
        self.line = frameLine

    def get_date(self, key) -> RusDate:
        return RusDate(self.line[key])

    def get_str(self, key) -> str:
        return self.line[key]

    def get_bool(self, key) -> bool:
        return self.line[key] != 0

    def get_int(self, key) -> int:
        return int(round(self.line[key]))

    def get_float(self, key) -> float:
        return self.line[key]


def get_frame(sql: str, connection=None, params: Dict = None):
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


def get_lines(sql: str, params: Dict = None, connection=None) -> List[DbLine]:
    frm = get_frame(sql, connection, params)
    return [DbLine(frm.iloc[i]) for i in range(len(frm.values))]


def get_line(sql: str, params: Dict = None, connection=None) -> DbLine:
    try:
        return get_lines(sql, params, connection)[0]
    except IndexError:
        raise NotFoundException()


def get_date(sql: str, params: Dict = None, connection=None) -> RusDate:
    return get_line(sql, params, connection).get_date(0)


def get_dates(sql: str, params: Dict = None, connection=None) -> List[RusDate]:
    frm, key = _get_line_data(sql, params, connection)
    return [RusDate(value) for value in frm[key]]


def get_str(sql: str, params: Dict = None, connection=None) -> str:
    return get_line(sql, params, connection).get_str(0)


def get_strs(sql: str, params: Dict = None, connection=None) -> List[str]:
    frm, key = _get_line_data(sql, params, connection)
    return frm[key]


def get_bools(sql: str, params: Dict = None, connection=None) -> bool:
    return get_line(sql, params, connection).get_bool(0)


def get_bool(sql: str, params: Dict = None, connection=None) -> List[bool]:
    frm, key = _get_line_data(sql, params, connection)
    return [value != 0 for value in frm[key]]


def get_int(sql: str, params: Dict = None, connection=None) -> int:
    return get_line(sql, params, connection).get_int(0)


def get_ints(sql: str, params: Dict = None, connection=None) -> List[int]:
    frm, key = _get_line_data(sql, params, connection)
    return [round(value) for value in frm[key]]


def get_float(sql: str, params: Dict = None, connection=None) -> float:
    return get_line(sql, params, connection).get_float(0)


def get_floats(sql: str, params: Dict = None, connection=None) -> List[float]:
    frm, key = _get_line_data(sql, params, connection)
    return frm[key]


def _get_line_data(sql, params, connection):
    frm = get_frame(sql, connection, params)
    key = frm.keys()[0]
    return frm, key


def execute_command(sql: str, params=None, connection=None, is_commit=True):
    if connection is None:
        with DbConnection() as conn, DbCursor(conn) as cursor:
            _executeCommand(sql, params, conn, cursor, is_commit)
    else:
        with DbCursor(connection) as cursor:
            _executeCommand(sql, params, connection, cursor, is_commit)


def insert(table: str, fields_with_values: dict, connection=None, is_commit=True, is_next_id_by_hand: bool = False):
    """
    Добавить запись в таблицу
    :param table:
    :param fields_with_values:
    :param connection:
    :param is_commit:
    :param is_next_id_by_hand: если True, можно получить id таблицы для дальнейшего использования
    :return: id добавленой записи, или -1, если is_next_id_by_hand = False
    """
    next_id = -1
    if is_next_id_by_hand:
        seq_name = f'seq_{table}_f_id'
        sql = f"select nextval('{seq_name}')"
        next_id = get_int(sql, connection=connection)
        fields_with_values['f_id'] = next_id
    sql, params = sqltools.sql_with_values_for_insert(table, fields_with_values)
    execute_command(sql, params, connection, is_commit)
    return next_id


def update(table: str, fields_with_values: dict, id: int, connection=None, is_commit=True):
    """Обновить запись в таблице
       where может быть выражением типа 'f_num_doc = 34454',
       а может быть целым числом. Тогда преобразуется в f_id = 10
    """
    sql, params = sqltools.sql_with_values_for_update(table, fields_with_values, id)
    execute_command(sql, params, connection, is_commit)


def _executeCommand(sql, params, conn, cursor, is_commit):
    # print(sql)
    # print(params)
    if params is None:
        params = ()
    try:
        cursor.execute(sql, params)
    except:
        if is_commit:
            conn.rollback()
        raise
    else:
        if is_commit:
            conn.commit()


if __name__ == '__main__':
    try:
        params = {
            'sclad': 3,
            'date_doc': RusDate('17/03/2020').for_sql(),
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

        lines = get_lines(sql, params)
        for line in lines:
            print(line.get_int(0), line.get_date("f_date_doc"), line.get_str('f_num_doc'),
                  line.get_bool("f_is_ready"),
                  line.get_str("sclad_name"))

        lines = get_lines("select f_cod, f_name from spr_scl")
        for line in lines:
            print(line.get_int(0), line.get_str(1))

        line = get_line("select f_cod, f_name from spr_scl where f_id = 1")
        print(line.get_int(0), line.get_str(1))

        with DbConnection() as conn:
            print(get_bools("select f_is_ready from docs where f_id = {{id}}", {'id': 2}, conn))
            print(get_str("select f_name from spr_scl where f_id = {{id}}", {'id': 1}, conn))
            print(get_date("select max(f_date_doc) from docs", connection=conn))
            print(get_float("select avg(f_id) from docs", connection=conn))
            ids = get_frame("select f_id, f_num_doc from docs", connection=conn)['f_id']
            print(ids.sum(), ids.min(), ids.max())
            frm = get_frame("select f_id, f_num_doc, f_sclad from docs", connection=conn)
            print(frm.eval('x = f_id + 100'))
            print(frm.groupby(['f_sclad']).max())

        ################################################################
        # update and insert
        fields = {
            'f_num_doc': 'Б14',
            'f_date_doc': RusDate.present_date(),
            'f_sclad': 1,
            'f_is_ready': 0
        }
        insert('docs', fields)

        fields = {
            'f_num_doc': 'Б15',
            'f_date_doc': RusDate.present_date(),
            'f_sclad': 1,
            'f_is_ready': 0
        }
        id = insert('docs', fields, is_next_id_by_hand=True)
        # Для последующего использования
        print(id)

        fields = {
            'f_date_doc': RusDate.present_date() - 100,
            'f_sclad': 2,
            'f_is_ready': 1
        }
        update('docs', fields, 11)
    except Exception as e1:
        print(str(e1))
