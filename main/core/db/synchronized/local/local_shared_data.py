# -*- coding: utf8 -*-

import threading


class LocalSharedData:
    _data = dict()
    _lock = dict()
    _lock_handle_lock = threading.Lock()

    @classmethod
    def _get_lock(cls, user_id: int) -> threading.Lock():
        with cls._lock_handle_lock:
            if user_id not in cls._lock.keys():
                cls._lock[user_id] = threading.Lock()
            result = cls._lock[user_id]
        return result

    @classmethod
    def get(cls, user_id: int, path: tuple = tuple()) -> object:
        with cls._get_lock(user_id):
            result = cls._data.get(user_id)
            if result is not None:
                for directory in path:
                    if type(result) is dict:
                        result = result.get(directory)
                    else:
                        result = None
                        break
        return result

    @classmethod
    def set(cls, user_id: int, value, path: tuple) -> dict:
        with cls._get_lock(user_id):
            if user_id not in cls._data.keys():
                cls._data[user_id] = dict()
            result = cls._data.get(user_id)
            for directory_num in range(len(path) - 1):
                directory = path[directory_num]
                if directory not in result.keys():
                    result[directory] = dict()
                result = result.get(directory)
            if len(path) > 0:
                result[path[-1]] = value
            else:
                value = None
        return value

    @classmethod
    def getset(cls, user_id: int, value, path: tuple) -> dict:
        with cls._get_lock(user_id):
            result_get = cls._data.get(user_id)
            if result_get is not None:
                for directory in path:
                    if type(result_get) is dict:
                        result_get = result_get.get(directory)
                    else:
                        result_get = None
                        break
            if user_id not in cls._data.keys():
                cls._data[user_id] = dict()
            result_set = cls._data.get(user_id)
            for directory_num in range(len(path) - 1):
                directory = path[directory_num]
                if directory not in result_set.keys():
                    result_set[directory] = dict()
                result_set = result_set.get(directory)
            if len(path) > 0:
                result_set[path[-1]] = value
        return result_get

    @classmethod
    def remove(cls, user_id: int, path: tuple = tuple()) -> dict:
        with cls._get_lock(user_id):
            value = None
            result = cls._data.get(user_id)
            if result is not None:
                if len(path) > 0:
                    for directory_num in range(len(path) - 1):
                        directory = path[directory_num]
                        if type(result) is dict:
                            result = result.get(directory)
                        else:
                            result = None
                            break
                    if result is not None and len(path) > 0:
                        value = result.get(path[-1])
                        if path[-1] in result.keys():
                            result.pop(path[-1])
                        else:
                            value = None
                else:
                    value = cls._data.pop(user_id)
        return value
