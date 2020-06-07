# -*- coding: utf8 -*-

import threading


class Singleton:
    _data = None
    _lock = threading.Lock()

    @classmethod
    def get(cls) -> type(_data):
        with cls._lock:
            result = cls._data
        return result

    @classmethod
    def set(cls, value):
        with cls._lock:
            cls._data = value
        return value

    @classmethod
    def getset(cls, value) -> type(_data):
        with cls._lock:
            result = cls._data
            cls._data = value
        return result
