from tools import StrTools
import statistics

from tools.exceptions import NotFoundException


def arrToStr(arr, sep=',', funcForStr=None) -> str:
    """Массив привести к строке с разделителями"""
    f = str if funcForStr is None else funcForStr
    return sep.join([f(item) for item in arr])


def empty(arr) -> bool:
    """Проверка на пустой маасив"""
    return False if arr else True


def notEmpty(arr) -> bool:
    """Проверка на непустой массив"""
    return not empty(arr)


def arrToStrArr(arr, funcForStr=None):
    """Массив чисел и т.п. привести к массиву строк"""
    f = str if funcForStr == None else funcForStr
    return [f(item) for item in arr]


def strArrToDigArr(arr):
    """Массив строк из чисел привести к массиву чисел"""
    return [eval(item) for item in arr]


def strArrFromString(str: str, sep: str = ','):
    """Массив строк от строки, в которой значения перечислены через разделитель"""
    return str.split(sep)


def digArrFromString(str: str, sep: str = ','):
    """Массив чисел от строки, в которой значения перечислены через разделитель"""
    return [eval(item) for item in str.split(sep)]


def maxLineLength(arr) -> int:
    """Длина самой длинной строки в массиве"""
    return max(len(item) for item in arr)


def padr(arr, len_: int, symb: str = ' '):
    """Массив строк, добитый симвлом справа до длины"""
    return [StrTools.padr(item, len_, symb) for item in arr]


def trim(arr):
    """Массив строк, с убранными хвостовыми и лидирующими пробелами"""
    return [StrTools.trim(item) for item in arr]


def rtrim(arr):
    """Массив строк, с убранными хвостовыми пробелами"""
    return [StrTools.rtrim(item) for item in arr]


def indexInArr(arr, v):
    """Номер элемента в массиве"""
    try:
        index = arr.index(v)
    except:
        index = -1
    return index


def arrToSet(arr):
    """массив в множество"""
    return set(arr)


def toUpperCase(arr):
    """массив к верхнему регистру"""
    return [item.upper() for item in arr]


def toLowerCase(arr):
    """массив к нижнему регистру"""
    return [item.lower() for item in arr]


def padrToMax(arr):
    """добить пробелами справа до длины самого длинного элемента"""
    ln = maxLineLength(arr)
    return padr(arr, ln)


def isInArray(arr, v) -> bool:
    """Проверяет наличие элемента в массиве"""
    return indexInArr(arr, v) > 0


def isInArrayByContains(arr, v) -> bool:
    """Проверяет наличие жлемента в массиве по принципу 'строка содержит'"""
    return len(list(filter(lambda item: v in item, arr))) > 0


def maxInArr(arr, funcForCalcMax=None):
    """Максимальное значение"""
    if (funcForCalcMax == None):
        return max(arr)
    return max([funcForCalcMax(item) for item in arr])


def minInArr(arr, funcForCalcMax=None):
    """Минимальное значение"""
    if (funcForCalcMax == None):
        return min(arr)
    return min([funcForCalcMax(item) for item in arr])


def meanInArr(arr, funcForCalcMean=None):
    """Среднее значение"""
    if funcForCalcMean == None:
        return statistics.mean(arr)
    if not arr:
        return 0
    return sum([funcForCalcMean(item) for item in arr]) / len(arr)


def swap(arr):
    """Перевернуть массив"""
    return list(reversed(arr))


def first(arr):
    """Первый элемент"""
    if not arr:
        raise NotFoundException()
    return list(arr)[0]


def last(arr):
    """Последний элемент"""
    if not arr:
        raise NotFoundException()
    return list(arr)[-1]


def next(arr, fromElement):
    """Следующий элемент от заданного"""
    isFound = False
    for el in arr:
        if el == fromElement:
            isFound = True
            continue
        if isFound:
            return el
    raise NotFoundException()


def prev(arr, fromElement):
    """Предыдущий элемент от заданного"""
    prevElement = None
    for el in arr:
        if el == fromElement:
            if prevElement == None:
                raise NotFoundException()
            return prevElement
        prevElement = el
    raise NotFoundException()


def getFilteredArr(arr, filterFunc):
    """Отфильтрованный массив"""
    return list(filter(filterFunc, arr))


def isAllEmpty(arr):
    """Все ли элементы пустые"""
    return len(getFilteredArr(arr, lambda x: not StrTools.empty(x))) == 0


def size(arr, filterFunc=None):
    """Количество элементов, удовлетворяющих фильтру"""
    if filterFunc == None:
        return len(arr)
    return len(getFilteredArr(arr, filterFunc))


def isOneOf(arr, el) -> bool:
    """Элемент - Один из массива"""
    return isInArray(arr, el)


def isNoOneOf(arr, el) -> bool:
    """Элемент - Ни один из массива"""
    return not isOneOf(arr, el)


def intersection(arr1, arr2):
    """Пересечение уникальных значений"""
    return list(set(arr1) & set(arr2))


def union(arr1, arr2):
    """Объедингение уникальных значений"""
    return list(set(arr1 + arr2))


if __name__ == '__main__':
    print('arrToStr([1,2,3,4]) = ', arrToStr([1, 2, 3, 4]))
    print('arrToStr(["a", "b", "c", "d"], "<BR>") = ', arrToStr(["a", "b", "c", "d"], "<BR>"))
    print('empty([]) = ', empty([]))
    print('arrToStrArr([1,2,3,4]) = ', arrToStrArr([1, 2, 3, 4]))
    print('strArrToDigArr(["1","2","3","4"]) = ', strArrToDigArr(["1", "2", "3", "4"]))
    print('strArrFromString("1,2,3,4") = ', strArrFromString("1,2,3,4"))
    print('digArrFromString("1,2,3,4") = ', digArrFromString("1,2,3,4"))
    print('maxLineLength(["as", "ert", "sssss"]) = ', maxLineLength(["as", "ert", "sssss"]))
    print('padr(["as", "ert", "sssss"], 10) = ', padr(["as", "ert", "sssss"], 10))
    print('trim([" as   ", "ert   ", "sssss   "]) = ', trim([" as   ", "ert   ", "sssss   "]))
    print('rtrim([" as   ", "ert   ", "sssss   "]) = ', rtrim([" as   ", "ert   ", "sssss   "]))
    print('indexInArr([" as   ", "ert   ", "sssss   "], "ert   ") = ',
          indexInArr([" as   ", "ert   ", "sssss   "], "ert   "))
    print('arrToSet([1,2,2,3,4,4]) = ', arrToSet([1, 2, 2, 3, 4, 4]))
    print('toUpperCase([" as   ", "ert   ", "sssss   "]) = ', toUpperCase([" as   ", "ert   ", "sssss   "]))
    print('toLowerCase([" AS   ", "ert   ", "sssss   "]) = ', toLowerCase([" AS   ", "ert   ", "sssss   "]))
    print('padrToMax(["as", "ert", "sssss"]) = ', padrToMax(["as", "ert", "sssss"]))
    print('isInArray([" as   ", "ert   ", "sssss   "], "ert   ") = ',
          isInArray([" as   ", "ert   ", "sssss   "], "ert   "))
    print('isInArrayByContains([" as   ", "ert   ", "sssss   "], "ss   ") = ',
          isInArrayByContains([" as   ", "ert   ", "sssss   "], "ss   "))
    print('maxInArr([1, 2, 2, 3, 4, 4], lambda x: 1 / x) = ', maxInArr([1, 2, 2, 3, 4, 4], lambda x: 1 / x))
    print('minInArr([1, 2, 2, 3, 4, 4], lambda x: 1 / x) = ', minInArr([1, 2, 2, 3, 4, 4], lambda x: 1 / x))
    print('meanInArr([1, 2, 2, 3, 4, 4], lambda x: 1 / x) = ', meanInArr([1, 2, 2, 3, 4, 4], lambda x: 1 / x))
    print('swap([1, 2, 2, 3, 4, 4]) = ', swap([1, 2, 2, 3, 4, 4]))
    print('first({1, 2, 2, 3, 4, 4}) = ', first({1, 2, 2, 3, 4, 4}))
    print('last({1, 2, 2, 3, 4, 4}) = ', last({1, 2, 2, 3, 4, 4}))
    try:
        print('next({1, 2, 2, 3, 4, 4}, 3) = ', next({1, 2, 2, 3, 4, 4}, 3))
    except NotFoundException:
        print('NotFoundException')
    try:
        print('prev({1, 2, 2, 3, 4, 4}, 3) = ', prev({1, 2, 2, 3, 4, 4}, 3))
    except NotFoundException:
        print('NotFoundException')
    print('getFilteredArr([1, 2, 2, 3, 4, 4], lambda x: x >2) = ', getFilteredArr([1, 2, 2, 3, 4, 4], lambda x: x > 2))
    print('isAllEmpty(["  ", "   "]) = ', isAllEmpty(["  ", "   "]))
    print('size([1, 2, 2, 3, 4, 4], lambda x: x >2) = ', size([1, 2, 2, 3, 4, 4], lambda x: x > 2))
    print('isOneOf([1,2,3,4], 3) = ', isOneOf([1, 2, 3, 4], 3))
    print('isNoOneOf([1,2,3,4], 3) = ', isNoOneOf([1, 2, 3, 4], 3))
    print('intersection([1,2,3,4], [3,4,5,6]) = ', intersection([1, 2, 3, 4], [3, 4, 5, 6]))
    print('union([1,2,3,4], [3,4,5,6]) = ', union([1, 2, 3, 4], [3, 4, 5, 6]))
