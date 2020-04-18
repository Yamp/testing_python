import string
def space(len):
    """return строку из len пробелов"""
    return ' ' * len


def repl(str: str, len: int) -> str:
    """return Возвращает строку, реплицированную символом до заданной длины"""
    return str * len


def empty(str: str) -> bool:
    """Проверка на пустую строку"""
    if str == None:
        return True
    if str == '' or str.isspace():
        return True
    return False


def notEmpty(str: str) -> bool:
    """Проверка на пустую строку"""
    return not empty(str)


def left(str: str, len_: int) -> str:
    """return Левая часть строки"""
    return str[:len_] if len(str) > len_ else str


def right(str: str, len_: int) -> str:
    """return Правая часть строки"""
    return str[-len_:] if len(str) > len_ else str


def padr(str: str, len_: int, symb: str = ' ') -> str:
    """Добивка символом справа"""
    strLen = len(str)
    return str if strLen > len_ else str + symb * (len_ - strLen)


def padl(str: str, len_: int, symb: str = ' ') -> str:
    """Добивка символом слева"""
    strLen = len(str)
    return str if strLen > len_ else symb * (len_ - strLen) + str


def padc(str: str, len_: int, symb: str = ' ') -> str:
    """Добивка пробелами для центровки"""
    strLen = len(str)
    if strLen > len_:
        return str
    else:
        q = len_ - strLen
        l = int(q / 2)
        r = q - l
        return symb * l + str + symb * r


def rtrim(str: str) -> str:
    """return убрать хвостовые пробелы"""
    return str.rstrip()


def ltrim(str: str) -> str:
    """return убрать лидирующие пробелы"""
    return str.lstrip()


def trim(str: str) -> str:
    """убрать хвостовые и лидирующие пробелы"""
    return str.strip()


def gripe(str: str) -> str:
    """убрать все пробелы"""
    return str.replace(' ', '')


def charone(str: str) -> str:
    """Сжать строку. Удалить повторяющиеся пробелы"""
    s = ''
    prevSplit = '@'
    for split in str.split(' '):
        if split != '' or prevSplit != '':
            if split == '':
                s += ' '
            s += split
        prevSplit = split
    return s


def FIO(str: str) -> str:
    """ФИО"""
    splits = str.split(' ')
    if len(splits) == 3:
        return f'{splits[0]} {splits[1][:1]}.{splits[2][:1]}.'
    else:
        s = ''
        for i in range(len(splits)):
            if i == 0:
                s += splits[i] + ' '
            else:
                s += splits[i][:1] + '.'
        return s


def equalsWithTrim(str1: str, str2: str):
    """Сравнить строки с обрезанием лидирующмх и хвостовых пробелов"""
    return str1.strip() == str2.strip()

def equalsIgnoreCase(str1: str, str2: str):
    """Сравнить строки игнорируя case"""
    return str1.lower() == str2.lower()


if (__name__ == '__main__'):
    print("space(10) = '" + space(10) + "'")
    print("repl('abc', 10) = " + repl('abc', 10))
    print("empty('   ') = " + str(empty('   ')))
    print("notEmpty('   ') = " + str(notEmpty('')))
    print("left('abcde', 3) = " + left('abcde', 3))
    print("right('abcde', 3) = " + right('abcde', 3))
    print("padr('abcde', 10, 'x') = " + padr('abcde', 10, 'x'))
    print("padr('abcde', 10) = " + padr('abcde', 10) + ";")
    print("padl('abcde', 10, 'x') = " + padl('abcde', 10, 'x'))
    print("padl('abcde', 10) = " + ";" + padl('abcde', 10) + ";")
    print("padc('abcde', 10, 'x') = " + padc('abcde', 10, 'x'))
    print("rtrim('  abcde    ') = " + ";" + rtrim('  abcde    ') + ";")
    print("ltrim('  abcde    ') = " + ";" + ltrim('  abcde    ') + ";")
    print("trim('  abcde    ') = " + ";" + trim('  abcde    ') + ";")
    print("gripe(' a  bcde    ') = " + ";" + gripe(' a  bcde    ') + ";")
    print("charone(' a  bcde    ') = " + ";" + charone(' a  bcde    ') + ";")
    print("FIO('Ямпольский Владимир Иосифович') = " + FIO('Ямпольский Владимир Иосифович'))
    print("equalsWithTrim('  jhg ', 'jhg ') = " + str(equalsWithTrim('  jhg ', 'jhg ')))
    print("equalsIgnoreCase('ОРПРОП', 'ОРпрОП') = " + str(equalsIgnoreCase('ОРПРОП', 'ОРпрОП')))
