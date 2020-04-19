import re


def space(n: int) -> str:
    """ return строку из len пробелов """

    # TODO: len перекрывает стандартную функцию len, лучше называть аргументы по друугому
    return ' ' * n


def repl(s: str, n: int) -> str:
    """ return Возвращает строку, реплицированную символом до заданной длины """

    return s * n


def empty(s: str) -> bool:
    """ Проверка на пустую строку """
    return not s or s.isspace()


def notEmpty(s: str) -> bool:
    """ Проверка на пустую строку """

    # TODO: почему бы не писать просто not empty(str)?
    return not empty(s)


def left(s: str, n: int) -> str:
    """ return Левая часть строки """

    # TODO: проще прямо так и писать в коде...
    return s[:n]


def right(s: str, n: int) -> str:
    """ return Правая часть строки """

    return s[-n:]


def padr(s: str, n: int, symb: str = ' ') -> str:
    """ Добивка символом справа """
    # или так s.ljust(n, symb)
    return f"{s:{symb}<{n}}"


def padl(s: str, n: int, symb: str = ' ') -> str:
    """ Добивка символом слева """
    # return s.rjust(n, symb)
    return f"{s:{symb}>{n}}"


def padc(s: str, n: int, symb: str = ' ') -> str:
    """ Добивка пробелами для центровки """
    # return s.center(n, symb)
    return f"{s:{symb}^{n}}"


def rtrim(s: str) -> str:
    """ return убрать хвостовые пробелы """
    return s.rstrip()


def ltrim(s: str) -> str:
    """ return убрать лидирующие пробелы """
    return s.lstrip()


def trim(s: str) -> str:
    """ Убрать хвостовые и лидирующие пробелы """
    return s.strip()


def gripe(s: str) -> str:
    """убрать все пробелы"""
    return s.replace(' ', '')


def charone(s: str) -> str:
    """Сжать строку. Удалить повторяющиеся пробелы"""
    return re.sub(r'\W+', ' ', s)


def FIO(s: str) -> str:
    """ ФИО (из может быть не 3) """
    assert not s.isspace(), 'Пустая строка'

    splits = s.split()
    return f'{splits[0]} {".".join(s[0] for s in splits[1:])}.'

    # TODO: оставил самый крутой вариант, в еще можно было использовать функцию enumerate
    # s = ''
    # for i, sp in enumerate(splits):
    #     if i == 0:
    #         s += splits[i] + ' '
    #     else:
    #         s += splits[i][:1] + '.'
    # return s


def equalsWithTrim(str1: str, str2: str):
    """Сравнить строки с обрезанием лидирующмх и хвостовых пробелов"""
    return str1.strip() == str2.strip()


def equalsIgnoreCase(str1: str, str2: str):
    """Сравнить строки игнорируя case"""

    # TODO: Твой вариант мог не работать со сложными юникод-символами.
    # TODO: Тут подробнее https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
    return str1.casefold() == str2.casefold()


if __name__ == '__main__':
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
