from typing import List, Any

from tools import strtools
from tools.rus_date import RusDate
from datetime import datetime, date, timedelta


def for_sql(value, null_if_zero=False, date_as_string: bool = False) -> str:
    """Выржение для подставноки в запрос"""
    if isinstance(value, bool):
        return str(1 if value else 0)
    elif isinstance(value, (int, float)):
        if null_if_zero and value == 0:
            return 'null'
        return str(value)
    elif isinstance(value, str):
        if (strtools.empty(value)):
            return "' '"
        s = strtools.rtrim(value)
        s = s.replace("'", "''").replace("%", "%%")
        return "'" + s + "'"
    elif type(value).__name__ in ('datetime', 'date'):
        return value
    elif type(value).__name__ == 'RusDate':
        return value.for_sql(date_as_string)


def for_param(value, null_if_zero=False) -> Any:
    """Выржение для подставноки в запрос"""
    if isinstance(value, bool):
        return 1 if value else 0
    elif isinstance(value, (int, float)):
        if null_if_zero and value == 0:
            return None
        return value
    elif isinstance(value, str):
        if strtools.empty(value):
            return ' '
        s = strtools.rtrim(value)
        return s.replace("'", "''").replace("%", "%%")
    elif type(value).__name__ in ('datetime', 'date'):
        return value
    elif type(value).__name__ == 'RusDate':
        return value.for_sql()


def to_between(field: str, from_val, to_val) -> str:
    """Выржение для between"""
    return " ( " + field + " between " + for_sql(from_val, date_as_string=True) \
           + " and " + for_sql(to_val, date_as_string=True) + " ) "


def to_in(field: str, *values, with_not=False) -> str:
    """Выржение для In"""
    try:
        lst = list(*values)[0]
    except:
        lst = list(values)
    s = field
    if with_not:
        s += ' not'
    s += ' in ('
    s += ",".join([for_sql(x, date_as_string=True) for x in lst])

    s += ')'
    return s


def to_not_in(field: str, *values):
    """Выржение для not in"""
    return to_in(field, values, with_not=True)


def sql_with_values_for_insert(table: str, fields_with_values: dict) -> (str, List):
    """Выражение для insert с параметрами для подстановки"""
    fields = ','.join(fields_with_values.keys())
    values = ','.join(('%s',) * len(fields_with_values))
    sql = f'insert into {table} ({fields}) values ({values})'
    values = [for_param(x) for x in fields_with_values.values()]
    return sql, values


def sql_with_values_for_update(table: str, fields_with_values: dict, where: Any = '') -> (str, List):
    """Выражение для update с параметрами для подстановки.
       where может быть выражением типа 'f_num_doc = 34454',
       а может быть целым числом. Тогда преобразуется в f_id = 10
    """
    if isinstance(where, int):
        where = f'where f_id={where}'
    else:
        where = f'where {where}'
    join = ','.join([k + '=%s' for k in fields_with_values.keys()])
    sql = f'update {table} set {join} {where}'
    values = [for_param(x) for x in fields_with_values.values()]
    return sql, values


def to_case(expr: str, when_then_pairs: dict, default):
    """Выржение для case when"""
    s = 'case ' + expr + '\n'
    s += ''.join(['\twhen ' + k + ' then ' + for_sql(v) + '\n' for k, v in when_then_pairs.items()])
    s += '\telse ' + for_sql(default) + '\n'
    s += 'end\n'
    return s


if __name__ == '__main__':
    print(for_sql(121))
    print(for_sql(1.5))
    print(for_sql(True))
    print(for_sql("h%%el'lo"))
    print(for_sql(RusDate.present_date()))
    print(for_sql(datetime.now() - timedelta(days=3)))
    print(to_between('f_summa', 1.5, 5))
    print(to_between('f_summa', RusDate('15/05/20'), RusDate('25/05/20')))

    print(to_in("f_code", 1, 2, 3))
    print(to_not_in("f_name", ['a', 'b', 'ddd']))
    print(to_in("f_date", RusDate('15/05/20'), RusDate('25/05/20'), RusDate('31/05/20'), RusDate.empty_date()))

    d = {"f_id": 1, "f_num_doc": "25/4567", "f_date": RusDate('15/02/20'), "f_is_ready": True, "f_sclad": 3}
    print(sql_with_values_for_insert('d_sh', d))
    print(sql_with_values_for_update('d_sh', d))

    d = {"1": 'x10', "2": 'y33', "3": 'z45'}
    print(to_case('f_id', d, 100))
