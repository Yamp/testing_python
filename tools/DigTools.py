from tools import StrTools, DigToText

THOUSAND_SEPARATOR = " "


def roundDo(value: float, valRound: float) -> float:
    """Округлить до (например 0.01)"""
    if valRound == 0:
        valRound = 0.01
    return round(round(value / valRound) * valRound, decLength(value))


def decLength(dd: float) -> int:
    """Длина дробной части"""
    if dd == int(dd):
        decLen = 0
    else:
        s = str(dd)
        try:
            try:
                ind = s.index('.')
            except:
                ind = s.index(',')
        except:
            ind = -1
        decLen = 0 if ind == 0 else len(s[ind + 1:])

    return decLen


def strVal(value: float, dec: int = -1, len: int = 0) -> str:
    """
    Привести число к строке
    :param value: число
    :param dec: количество знаков после запятой
    :param len: длина строки
    :return:
    """
    d = value if dec == -1 else round(value, dec)
    s = str(d)
    if len > 0:
        s = StrTools.padl(s, len)
    return s


def strFlexible(value: float, dec: int = 2, isEmptyIfZero: bool = False) -> str:
    """Привести число к строке с плавающим количеством знаков после запятой"""
    if value == 0 and isEmptyIfZero:
        return ""
    v = round(value, dec)
    if v == int(v):
        return str(int(value))
    return str(v)


def between(value: float, fromV: float, toV: float, isInclusive: bool = True) -> bool:
    """Проверка на вхождлени числа в интервал"""
    if isInclusive:
        return value >= fromV and value <= toV
    else:
        return value > fromV and value < toV


def commaToDot(doubleDig: str) -> str:
    """Запятую заменить на точку"""
    return doubleDig.replace(',', '.')


def minVal(values) -> float:
    """Минимальное значение из списка"""
    return min(values)


def maxVal(values) -> float:
    """Максимальное значение из списка"""
    return max(values)


def isEven(value: float) -> float:
    """Проверка на четность"""
    v = value / 2
    return v == int(v)


def dig_to_text(value: float, isCopAsText: bool = False) -> str:
    """Число (деньги) привест  к тексту"""
    return DigToText.decimal2textRub(value, isCopAsText)


def separateDigit(value: float) -> str:
    """Число привести к строке с разделителями тысяч"""
    return '{:,}'.format(value).replace(',', THOUSAND_SEPARATOR)


if (__name__ == '__main__'):
    print('decLength(123) = ', decLength(123))
    print('decLength(123.45678) = ', decLength(123.45678))
    print('roundDo(123.45678, 0.01) = ', round(roundDo(123.45678, 0.01), 2))
    print('strVal(123.45678, 2) = ', strVal(123.45678, 2))
    print('strFlexible(123.45678, 2) = ', strFlexible(123.45678, 2))
    print('strFlexible(123.45678, 0) = ', strFlexible(123.45678, 0))
    print('strFlexible(123, 3) = ', strFlexible(123, 3))
    print('strFlexible(0, 3, False) = ', strFlexible(0, 3, False))
    print('strFlexible(0, 3, True) = ', strFlexible(0, 3, True))
    print('between(100, 90, 110) = ', between(100, 90, 110))
    print('commaToDot("123,456") = ', commaToDot("123,456"))
    print('isEven(4) = ', isEven(4))
    print('dig_to_text(105254.24)', dig_to_text(105254.24))
    print('separateDigit(105254.24)', separateDigit(105254.24))
