import json
from typing import List, Set, Dict, Any

from tools import strtools
import statistics

from tools.exceptions import NotFoundException


def arr2str(arr, sep=',', func_for_str=None) -> str:
    """Массив привести к строке с разделителями"""
    f = str if func_for_str is None else func_for_str
    return sep.join([f(item) for item in arr])


def empty(arr) -> bool:
    """Проверка на пустой маасив"""
    return len(arr) == 0


def arr2str_arr(arr, func_for_str=None):
    """Массив чисел и т.п. привести к массиву строк"""
    f = str if func_for_str is None else func_for_str
    return [f(item) for item in arr]


def str_arr2dig_arr(arr: List[str]) -> List[Any]:
    """Массив строк из чисел привести к массиву чисел"""
    return [json.loads(item) for item in arr]


def str_arr_from_str(s: str, sep: str = ','):
    """Массив строк от строки, в которой значения перечислены через разделитель"""
    return s.split(sep)


def dig_arr_from_str(s: str, sep: str = ','):
    """Массив чисел от строки, в которой значения перечислены через разделитель"""
    return [json.loads(item) for item in s.split(sep)]


def max_line_len(arr) -> int:
    """Длина самой длинной строки в массиве"""
    return max(len(item) for item in arr)


def padr(arr, len_: int, symb: str = ' '):
    """Массив строк, добитый симвлом справа до длины"""
    return [strtools.padr(item, len_, symb) for item in arr]


def trim(arr):
    """Массив строк, с убранными хвостовыми и лидирующими пробелами"""
    return [strtools.trim(item) for item in arr]


def rtrim(arr):
    """Массив строк, с убранными хвостовыми пробелами"""
    return [strtools.rtrim(item) for item in arr]


def index_in_arr(arr, v):
    """Номер элемента в массиве"""
    try:
        index = arr.index(v)
    except ValueError:
        index = -1
    return index


def arr2set(arr):
    """массив в множество"""
    return set(arr)


def to_upper(arr):
    """массив к верхнему регистру"""
    return [item.upper() for item in arr]


def to_lower(arr):
    """массив к нижнему регистру"""
    return [item.lower() for item in arr]


def padr2max(arr):
    """добить пробелами справа до длины самого длинного элемента"""
    ln = max_line_len(arr)
    return padr(arr, ln)


def is_in_array(arr, v) -> bool:
    """Проверяет наличие элемента в массиве"""
    return v in arr


def is_in_arr_by_contains(arr, v) -> bool:
    """Проверяет наличие жлемента в массиве по принципу 'строка содержит'"""
    return any(v in a for a in arr)


def max_in_arr(arr, func_for_calc_max=lambda x: x):
    """Максимальное значение"""
    return max(func_for_calc_max(item) for item in arr)


def min_in_arr(arr, func_for_calc_min=lambda x: x):
    """Минимальное значение"""
    return min(func_for_calc_min(item) for item in arr)


def mean_in_arr(arr, func_for_calc_mean=lambda x: x):
    """Среднее значение"""
    if not arr:
        return 0
    return sum(func_for_calc_mean(item) for item in arr) / len(arr)


def swap(arr: List) -> List:
    """Перевернуть массив"""
    return list(reversed(arr))


def first(arr):
    """Первый элемент"""
    if not arr:
        raise NotFoundException()
    if isinstance(arr, List):
        return arr[0]
    return list(arr)[0]


def last(arr):
    """Последний элемент"""
    if not arr:
        raise NotFoundException()
    if isinstance(arr, List):
        return arr[-1]
    return list(arr)[-1]


def next_val(arr, from_val):
    """Следующий элемент от заданного"""
    if not isinstance(arr, List):
        arr = list(arr)
    i = arr.index(from_val)
    return arr[i + 1]


def prev_val(arr, from_val):
    """Предыдущий элемент от заданного"""
    if not isinstance(arr, List):
        arr = list(arr)
    arr = list(arr)
    i = arr.index(from_val)
    return arr[i - 1]


def filtered_arr(arr, filter_func):
    """Отфильтрованный массив"""
    return list(filter(filter_func, arr))


def is_all_empty(arr):
    """ Все ли элементы пустые """
    return all(strtools.empty(e) for e in arr)


def size(arr, filter_func=None):
    """Количество элементов, удовлетворяющих фильтру"""
    if filter_func is None:
        return len(arr)
    return len(filtered_arr(arr, filter_func))


def is_one_of(arr, el) -> bool:
    """Элемент - Один из массива"""
    return is_in_array(arr, el)


def is_no_one_of(arr, el) -> bool:
    """Элемент - Ни один из массива"""
    return not is_one_of(arr, el)


def intersection(arr1, arr2):
    """Пересечение уникальных значений"""
    return list(set(arr1) & set(arr2))


def union(arr1, arr2):
    """Объедингение уникальных значений"""
    return list(set(arr1 + arr2))


if __name__ == '__main__':
    print('arr2str([1,2,3,4]) = ', arr2str([1, 2, 3, 4]))
    print('(["a", "b", "c", "d"], "<BR>") = ', arr2str(["a", "b", "c", "d"], "<BR>"))
    print('empty([]) = ', empty([]))
    print('arr2str_arr([1,2,3,4]) = ', arr2str_arr([1, 2, 3, 4]))
    print('(["1","2","3","4"]) = ', str_arr2dig_arr(["1", "2", "3", "4"]))
    print('str_arr_from_str("1,2,3,4") = ', str_arr_from_str("1,2,3,4"))
    print('dig_arr_from_str("1,2,3,4") = ', dig_arr_from_str("1,2,3,4"))
    print('max_line_len(["as", "ert", "sssss"]) = ', max_line_len(["as", "ert", "sssss"]))
    print('padr(["as", "ert", "sssss"], 10) = ', padr(["as", "ert", "sssss"], 10))
    print('trim([" as   ", "ert   ", "sssss   "]) = ', trim([" as   ", "ert   ", "sssss   "]))
    print('rtrim([" as   ", "ert   ", "sssss   "]) = ', rtrim([" as   ", "ert   ", "sssss   "]))
    print('index_in_arr([" as   ", "ert   ", "sssss   "], "ert   ") = ',
          index_in_arr([" as   ", "ert   ", "sssss   "], "ert   "))
    print('arr2set([1,2,2,3,4,4]) = ', arr2set([1, 2, 2, 3, 4, 4]))
    print('to_upper([" as   ", "ert   ", "sssss   "]) = ', to_upper([" as   ", "ert   ", "sssss   "]))
    print('to_lower([" AS   ", "ert   ", "sssss   "]) = ', to_lower([" AS   ", "ert   ", "sssss   "]))
    print('padr2max(["as", "ert", "sssss"]) = ', padr2max(["as", "ert", "sssss"]))
    print('is_in_array([" as   ", "ert   ", "sssss   "], "ert   ") = ',
          is_in_array([" as   ", "ert   ", "sssss   "], "ert   "))
    print('is_in_arr_by_contains([" as   ", "ert   ", "sssss   "], "ss   ") = ',
          is_in_arr_by_contains([" as   ", "ert   ", "sssss   "], "ss   "))
    print('max_in_arr([1, 2, 2, 3, 4, 4], lambda x: 1 / x) = ', max_in_arr([1, 2, 2, 3, 4, 4], lambda x: 1 / x))
    print('min_in_arr([1, 2, 2, 3, 4, 4], lambda x: 1 / x) = ', min_in_arr([1, 2, 2, 3, 4, 4], lambda x: 1 / x))
    print('mean_in_arr([1, 2, 2, 3, 4, 4], lambda x: 1 / x) = ', mean_in_arr([1, 2, 2, 3, 4, 4], lambda x: 1 / x))
    print('swap([1, 2, 2, 3, 4, 4]) = ', swap([1, 2, 2, 3, 4, 4]))
    print('first({1, 2, 2, 3, 4, 4}) = ', first({1, 2, 2, 3, 4, 4}))
    print('last({1, 2, 2, 3, 4, 4}) = ', last({1, 2, 2, 3, 4, 4}))
    try:
        print('next_val({1, 2, 2, 3, 4, 4}, 3) = ', next_val({1, 2, 2, 3, 4, 4}, 3))
    except NotFoundException:
        print('NotFoundException')
    try:
        print('prev_val({1, 2, 2, 3, 4, 4}, 3) = ', prev_val({1, 2, 2, 3, 4, 4}, 3))
    except NotFoundException:
        print('NotFoundException')
    print('filtered_arr([1, 2, 2, 3, 4, 4], lambda x: x >2) = ', filtered_arr([1, 2, 2, 3, 4, 4], lambda x: x > 2))
    print('is_all_empty(["  ", "   "]) = ', is_all_empty(["  ", "   "]))
    print('size([1, 2, 2, 3, 4, 4], lambda x: x >2) = ', size([1, 2, 2, 3, 4, 4], lambda x: x > 2))
    print('is_one_of([1,2,3,4], 3) = ', is_one_of([1, 2, 3, 4], 3))
    print('is_no_one_of([1,2,3,4], 3) = ', is_no_one_of([1, 2, 3, 4], 3))
    print('intersection([1,2,3,4], [3,4,5,6]) = ', intersection([1, 2, 3, 4], [3, 4, 5, 6]))
    print('union([1,2,3,4], [3,4,5,6]) = ', union([1, 2, 3, 4], [3, 4, 5, 6]))
