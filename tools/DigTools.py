import locale
import math
from decimal import Decimal

from num2words import num2words

from tools import StrTools, DigToText

THOUSAND_SEPARATOR = " "


def strVal(value: float, dec: int = -1, n: int = 0) -> str:
    """
    Привести число к строке
    :param value: число
    :param dec: количество знаков после запятой
    :param n: длина строки
    :return:
    """
    # TODO: почитай, это полезно https://docs.python.org/3.4/library/string.html#format-string-syntax
    d = value if dec == -1 else round(value, dec)
    s = str(d)
    if n > 0:
        s = StrTools.padl(s, n)
    return s
    # return f'{value:{n}10.{dec}}f'


def strFlexible(value: float, dec: int = 2, isEmptyIfZero: bool = False) -> str:
    """ Привести число к строке с плавающим количеством знаков после запятой """
    if value == 0 and isEmptyIfZero:
        return ""
    v = round(value, dec)

    return str(int(value)) if v == int(v) else str(v)


def between(value: float, start: float, end: float, inclusive: bool = True) -> bool:
    """Проверка на вхождлени числа в интервал"""
    if inclusive and value in (start, end):
        return True

    return start < value < end


def commaToDot(doubleDig: str) -> str:
    """ Запятую заменить на точку """
    return doubleDig.replace(',', '.')


def minVal(values) -> float:
    """Минимальное значение из списка"""
    return min(values)


def maxVal(values) -> float:
    """Максимальное значение из списка"""
    return max(values)


def isEven(value: float) -> float:
    """Проверка на четность"""

    # TODO: для float это тоже сработает, но опять проблема округления. Можно указать точность
    return math.isclose(value % 2, 0)


def dig_to_text(value: float, isCopAsText: bool = False) -> str:
    """ Число (деньги) привести к тексту """

    # TODO: https://github.com/savoirfairelinux/num2words
    # TODO: Мб использовать вот это библиотеку. Кроме валют она умеет годы, порядковые числительные и еще что-то
    # num2words(value, lang='ru')
    # но валюту она только евро умеет :(

    return DigToText.decimal2textRub(value, isCopAsText)


def separateDigit(value: float) -> str:
    """ Число привести к строке с разделителями тысяч """
    # TODO: про локализациб чисел и тд:
    # https://stackoverflow.com/questions/13362121/convert-python-strings-into-floats-explicitly-using-the-comma-or-the-point-as-se
    # https://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators

    # locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    #
    # return f'{value:n}'
    # return locale.format_string("%.3f", value, grouping=True, monetary=True)
    # return locale.format_string("%.f", value, grouping=True, monetary=True)
    return '{:,}'.format(value).replace(',', THOUSAND_SEPARATOR)


if __name__ == '__main__':
    print(f'{strVal(123.45678, 2)=}')
    print(f'{strFlexible(123.45678, 2)=}')
    print(f'{strFlexible(123.45678, 0)=}')
    print(f'{strFlexible(123, 3)=}')
    print(f'{strFlexible(0, 3, False)=}')
    print(f'{strFlexible(0, 3, True)=}')
    print(f'{between(100, 90, 110)=}')
    print(f'{commaToDot("123,456")=}')
    print(f'{isEven(4)=}')
    print(f'{isEven(3)=}')
    print(f'{dig_to_text(105254.24)=}')
    print(f'{separateDigit(105254.24)=}')
