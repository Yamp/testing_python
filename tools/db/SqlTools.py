from typing import List, Any

from tools import StrTools
from tools.RusDate import RusDate
from datetime import datetime, date, timedelta


def forSql(value, nullIfZero=False, dateAsString: bool = False) -> str:
    """Выржение для подставноки в запрос"""
    if isinstance(value, bool):
        return str(1 if value else 0)
    elif isinstance(value, (int, float)):
        if nullIfZero and value == 0:
            return 'null'
        return str(value)
    elif isinstance(value, str):
        if (StrTools.empty(value)):
            return "' '"
        s = StrTools.rtrim(value)
        s = s.replace("'", "''").replace("%", "%%")
        return "'" + s + "'"
    elif type(value).__name__ in ('datetime', 'date'):
        return value
    elif type(value).__name__ == 'RusDate':
        return value.forSql(dateAsString)


def forParam(value, nullIfZero=False) -> Any:
    """Выржение для подставноки в запрос"""
    if isinstance(value, bool):
        return 1 if value else 0
    elif isinstance(value, (int, float)):
        if nullIfZero and value == 0:
            return None
        return value
    elif isinstance(value, str):
        if StrTools.empty(value):
            return ' '
        s = StrTools.rtrim(value)
        return s.replace("'", "''").replace("%", "%%")
    elif type(value).__name__ in ('datetime', 'date'):
        return value
    elif type(value).__name__ == 'RusDate':
        return value.forSql()


def toBetween(field: str, valFrom, valTo) -> str:
    """Выржение для between"""
    return " ( " + field + " between " + forSql(valFrom, dateAsString=True) + " and " + forSql(valTo,
                                                                                               dateAsString=True) + " ) "


def toInString(field: str, *values, withNot=False) -> str:
    """Выржение для In"""
    try:
        l = list(*values)[0]
    except:
        l = list(values)
    s = field
    if withNot:
        s += ' not'
    s += ' in ('
    s += ",".join([forSql(x, dateAsString=True) for x in l])

    s += ')'
    return s


def toNotInString(field: str, *values):
    """Выржение для not in"""
    return toInString(field, values, withNot=True)


def sqlWithValuesForInsert(table: str, fieldsWithValues: dict) -> (str, List):
    """Выражение для insert с параметрами для подстановки"""
    joinFields = ','.join(fieldsWithValues.keys())
    joinValues = ','.join(('%s',) * len(fieldsWithValues))
    sql = f'insert into {table} ({joinFields}) values ({joinValues})'
    values = [forParam(x) for x in fieldsWithValues.values()]
    return sql, values


def sqlWithValuesForUpdate(table: str, fieldsWithValues: dict, where: Any = '') -> (str, List):
    """Выражение для update с параметрами для подстановки.
       where может быть выражением типа 'f_num_doc = 34454',
       а может быть целым числом. Тогда преобразуется в f_id = 10
    """
    if isinstance(where, int):
        where = f'where f_id={where}'
    join = ','.join([k + '=%s' for k in fieldsWithValues.keys()])
    sql = f'update {table} set {join} {where}'
    values = [forParam(x) for x in fieldsWithValues.values()]
    return sql, values


def toCase(expr: str, whenThePairs: dict, defaultValue):
    """Выржение для case when"""
    s = 'case ' + expr + '\n'
    s += ''.join(['\twhen ' + k + ' then ' + forSql(v) + '\n' for k, v in whenThePairs.items()])
    s += '\telse ' + forSql(defaultValue) + '\n'
    s += 'end\n'
    return s


if __name__ == '__main__':
    print(forSql(121))
    print(forSql(1.5))
    print(forSql(True))
    print(forSql("h%%el'lo"))
    print(forSql(RusDate.presentDate()))
    print(forSql(datetime.now() - timedelta(days=3)))
    print(toBetween('f_summa', 1.5, 5))
    print(toBetween('f_summa', RusDate('15/05/20'), RusDate('25/05/20')))

    print(toInString("f_code", 1, 2, 3))
    print(toNotInString("f_name", ['a', 'b', 'ddd']))
    print(toInString("f_date", RusDate('15/05/20'), RusDate('25/05/20'), RusDate('31/05/20'), RusDate.emptyDate()))

    d = {"f_id": 1, "f_num_doc": "25/4567", "f_date": RusDate('15/02/20'), "f_is_ready": True, "f_sclad": 3}
    print(sqlWithValuesForInsert('d_sh', d))
    print(sqlWithValuesForUpdate('d_sh', d))

    d = {"1": 'x10', "2": 'y33', "3": 'z45'}
    print(toCase('f_id', d, 100))
