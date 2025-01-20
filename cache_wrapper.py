# Реализуйте lru_cache декоратор.
#
# Требования:
#
# - Декоратор должен кешировать результаты вызовов функции на основе её аргументов.
# - Если функция вызывается с теми же аргументами, что и ранее, возвращайте результат из кеша вместо повторного выполнения функции.
# - Декоратор должно быть возможно использовать двумя способами: с указанием максимального кол-ва элементов и без.

from functools import wraps
import unittest.mock
import my_module

def lru_cache(_func=None, *, maxsize=None):
    cache = dict()  # словарь, хранящий кэш
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_params = (args, tuple((kwargs.items())))   # получаем ключ из аргументов функции
            res = cache.get(func_params)

            if res:  # если кэш содержит результат функции, возвращаем
                return res
            res = func(*args, **kwargs)
            cache[func_params] = res

            if isinstance(maxsize, int):
                if len(cache) >= maxsize:  # если превышен размер кэша, удаляем первый элемент словаря
                    cache.pop(next(iter(cache)))
            return res

        return wrapper

    if _func is None:   # если декоратор вызван с аргументами
        return decorator
    else:
        return decorator(_func)


@lru_cache
def summ(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    assert summ(1, 2) == 3
    assert summ(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4