# -*- coding: utf8 -*-

from main.core.db.redis_app import db
import threading
import ast


class IdDictionary:
    _data = dict()
    _lock = dict()
    _lock_handle_lock = threading.Lock()
    _name = 'YourName'
    _redis_db_number = 14  # (стандарт)
    _redis_lock_db_number = 15  # (стандарт)

    @classmethod
    def _get_lock(cls, user_id: int) -> threading.Lock():
        with cls._lock_handle_lock:
            if user_id not in cls._lock.keys():
                cls._lock[user_id] = threading.Lock()
            result = cls._lock[user_id]
        return result


    @classmethod
    def get(cls, user_id: int) -> str:
        with cls._get_lock(user_id):
            if user_id not in cls._data.keys():
                cls._data[user_id] = '/'
            result = cls._data.get(user_id)
        return result

    @classmethod
    def set(cls, user_id: int, value: str) -> str:
        with cls._get_lock(user_id):
            cls._data[user_id] = str(value)
        return str(value)

    @classmethod
    def getset(cls, user_id: int, value: str) -> str:
        with cls._get_lock(user_id):
            if user_id not in cls._data.keys():
                cls._data[user_id] = '/'
            result = cls._data.get(user_id)
            cls._data[user_id] = str(value)
        return result

    @classmethod
    def remove(cls, user_id: int) -> str:
        with cls._get_lock(user_id):
            result = None
            if user_id in cls._data.keys():
                result = cls._data.pop(user_id)
        return result

    # TODO Оптимизация добавления элементов в словарь
    @classmethod
    def sync(cls):
        with cls._lock_handle_lock:
            lock = db[cls._redis_lock_db_number].lock(cls._name)
            with lock:
                update_value_bytes = db[cls._redis_db_number].hgetall(cls._name)
                update_value_str = {}
                for key, value in update_value_bytes.items():
                    try:
                        key = int(key.decode("utf-8"))
                        value = value.decode("utf-8")
                        update_value_str[key] = value
                    except:
                        pass
                update_value_str.update(cls._data)
                cls._data.update(update_value_str)
                print('{0}'.format(cls._data))
                if update_value_str.__len__() > 0:
                    db[cls._redis_db_number].hmset(cls._name, update_value_str)
        return
