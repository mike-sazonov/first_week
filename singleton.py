# Реализуйте паттерн синглтон тремя способами:
#
# - с помощью метаклассов
# - с помощью метода __new__ класса
# - через механизм импортов


#   Синглтон с помощью метода __new__ класса

class MySingleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            _instance = object.__new__(cls)
        return cls._instance


#   Синглтон с помощью метакласса

class MetaSingleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]
