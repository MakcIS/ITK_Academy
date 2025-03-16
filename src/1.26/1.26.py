from singleton import singleton3

class MetaSingleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super.__call__(cls, *args, **kwargs)
        return cls._instance[cls]
    
class Singleton1(metaclass=MetaSingleton):
    pass


class Singleton2:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
