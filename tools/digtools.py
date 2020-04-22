import locale
import math

from num2words import num2words

from tools import strtools

THOUSAND_SEPARATOR = " "


def str_val(value: float, dec: int = -1, n: int = 0) -> str:
    """
    Привести число к строке
    :param value: число
    :param dec: количество знаков после запятой
    :param n: длина строки
    :return:
    """
    d = value if dec == -1 else round(value, dec)
    s = str(d)
    if n > 0:
        s = strtools.padl(s, n)
    return s
    # return f'{value:{n}10.{dec}}f'


def str_flexible(value: float, dec: int = 2, is_empty_if_zero: bool = False) -> str:
    """ Привести число к строке с плавающим количеством знаков после запятой """
    if value == 0 and is_empty_if_zero:
        return ""
    v = round(value, dec)

    return str(int(value)) if v == int(v) else str(v)


def between(value: float, start: float, end: float, inclusive: bool = True) -> bool:
    """Проверка на вхождлени числа в интервал"""
    if inclusive and value in (start, end):
        return True

    return start < value < end


def comma2dot(value: str) -> str:
    """ Запятую заменить на точку """
    return value.replace(',', '.')


def is_even(value: float) -> float:
    """Проверка на четность"""
    return math.isclose(value % 2, 0)


def dig2text(value: float) -> str:
    return num2words(value, lang='ru', to='currency', currency="RUB")


def separateDigit(value: float) -> str:
    """ Число привести к строке с разделителями тысяч """
    return '{:,}'.format(value).replace(',', THOUSAND_SEPARATOR)


if __name__ == '__main__':
    print(f'{str_val(123.45678, 2)=}')
    print(f'{str_flexible(123.45678, 2)=}')
    print(f'{str_flexible(123.45678, 0)=}')
    print(f'{str_flexible(123, 3)=}')
    print(f'{str_flexible(0, 3, False)=}')
    print(f'{str_flexible(0, 3, True)=}')
    print(f'{between(100, 90, 110)=}')
    print(f'{comma2dot("123,456")=}')
    print(f'{is_even(4)=}')
    print(f'{is_even(3)=}')
    print(f'{dig2text(105254.24)=}')
    print(f'{separateDigit(105254.24)=}')
