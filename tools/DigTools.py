import locale
import math
from decimal import Decimal

from num2words import num2words

from tools import StrTools, DigToText

THOUSAND_SEPARATOR = " "


def roundDo(value: float, valRound: float) -> float:
    """Округлить до (например 0.01)"""
    # TODO: предлагаю сделать valRound строкой, чтобы избежать проблемы с float.
    # TODO: Или можно использовать Rational для дробей

    if valRound == 0:
        valRound = 0.01

    return round(valRound, decLength(value))


def decLength(dd: float) -> int:
    """ Длина дробной части """
    # TODO: Нужно что-то придумать с ошибками округления. 0.1 легко превращается в 0.099999999999999999...
    # TODO: в твоей реализации тоже была эта проблема. Лучше этой функцией вообще не пользоваться

    # Note that Decimal.from_float(0.1) is not the same as Decimal('0.1').
    # Since 0.1 is not exactly representable in binary floating point, the
    # value is stored as the nearest representable value which is
    # 0x1.999999999999ap-4.  The exact equivalent of the value in decimal
    # is 0.1000000000000000055511151231257827021181583404541015625.

    return -Decimal(dd).as_tuple().exponent


def strVal(value: float, dec: int = -1, n: int = 0) -> str:
    """
    Привести число к строке
    :param value: число
    :param dec: количество знаков после запятой
    :param n: длина строки
    :return:
    """
    # TODO: почитай, это полезно https://docs.python.org/3.4/library/string.html#format-string-syntax
    return f'{value:{n}.{dec}}f'


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

    locale.setlocale(locale.LC_ALL, '')

    # return f'{value:n}'
    # return locale.format_string("%.3f", value, grouping=True, monetary=True)
    return locale.format_string("%.f", value, grouping=True, monetary=True)


if __name__ == '__main__':
    print(f'{decLength(123)=}')
    print(f'{decLength(123.45678)=}')
    print(f'{roundDo(123.45678, 0.01)=}')
    print(f'{strVal(123.45678, 2)=}')
    print(f'{strFlexible(123.45678, 2)=}')
    print(f'{strFlexible(123.45678, 0)=}')
    print(f'{strFlexible(123, 3)=}')
    print(f'{strFlexible(0, 3, False)=}')
    print(f'{strFlexible(0, 3, True)=}')
    print(f'{between(100, 90, 110)=}')
    print(f'{commaToDot("123,456")=}')
    print(f'{isEven(4)=}')
    print(f'{dig_to_text(105254.24)=}')
    print(f'{separateDigit(105254.24)=}')
