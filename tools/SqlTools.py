from tools import StrTools
from tools.RusDate import RusDate
from datetime import datetime, date, timedelta


def forSql(value, nullIfZero=False) -> str:
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
        return "to_date('" + str(value.year) + '-' + StrTools.padl(str(value.month), 2, '0') + '-' + StrTools.padl(
            str(value.day), 2, '0') + "', 'YYYY-MM-DD')"
    elif type(value).__name__ == 'RusDate':
        if value.empty():
            return "null"
        return "to_date('" + str(value.getYear()) + '-' + StrTools.padl(str(value.getMonth()), 2,
                                                                        '0') + '-' + StrTools.padl(str(value.getDay()),
                                                                                                   2,
                                                                                                   '0') + "', 'YYYY-MM-DD')"


def toBetween(field: str, valFrom, valTo) -> str:
    """Выржение для between"""
    return " ( " + field + " between " + forSql(valFrom) + " and " + forSql(valTo) + " ) "


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
    s += ",".join([forSql(x) for x in l])

    s += ')'
    return s


def toNotInString(field: str, *values):
    """Выржение для not in"""
    return toInString(field, values, withNot=True)


def sqlForInsert(fieldWithValues: dir, table: str) -> str:
    """Выржение для insert"""
    return 'insert into ' + table + '(' + ','.join(fieldWithValues.keys()) + ') values (' + ','.join(
        [forSql(x) for x in fieldWithValues.values()]) + ')'


def sqlForUpdate(fieldWithValues: dir, table: str) -> str:
    """Выржение для update"""
    return 'update ' + table + ' set ' + ','.join([k + '=' + forSql(v) for k, v in fieldWithValues.items()])


def toCase(expr:str, whenThePairs:dir, defaultValue):
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

    d = {"f_id": 1, "f_num_doc": "25/4567", "f_date": RusDate('15/02/20')}
    print(sqlForInsert(d, 'd_sh'))
    print(sqlForUpdate(d, 'd_sh'))

    d = {"1": 'x10', "2": 'y33', "3": 'z45'}
    print(toCase('f_id', d, 100))
