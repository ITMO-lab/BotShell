# -*- coding: utf8 -*-

from main.core.db.redis_app import db
import threading
import ast


class IdSet:
    _lock = threading.Lock()
    _data = set()
    _name = 'YourName'
    _redis_db_number = 14
    _redis_lock_db_number = 15

    @classmethod
    def user_add(cls, user_id: int) -> bool:
        with cls._lock:
            cls._data.add(user_id)
            result = user_id in cls._data
        return result

    @classmethod
    def users_add(cls, users_id: list) -> bool:
        with cls._lock:
            result = True
            for element in users_id:
                if type(element) is not int:
                    result = False
                    break
            if result:
                cls._data.update(users_id)
                result = set(users_id).issubset(cls._data)
        return result

    @classmethod
    def user_remove(cls, user_id: int) -> bool:
        with cls._lock:
            lock = db[cls._redis_lock_db_number].lock(cls._name)
            with lock:
                db[cls._redis_db_number].srem(cls._name, str(user_id))
                if user_id in cls._data:
                    cls._data.remove(user_id)
                result = user_id in cls._data
        return result

    @classmethod
    def users_remove(cls, users_id: list) -> bool:
        with cls._lock:
            result = True
            for element in users_id:
                if type(element) is not int:
                    result = False
                    break
            if result:
                lock = db[cls._redis_lock_db_number].lock(cls._name)
                with lock:
                    db[cls._redis_db_number].srem(cls._name, *users_id)
                    cls._data.difference_update(users_id)
                    result = cls._data.intersection(users_id).__len__() == 0
        return result

    @classmethod
    def user_find(cls, user_id: int) -> bool:
        with cls._lock:
            result = user_id in cls._data
        return result

    # TODO Оптимизация добавления элементов во множества
    @classmethod
    def sync(cls):
        with cls._lock:
            lock = db[cls._redis_lock_db_number].lock(cls._name)
            with lock:
                update = db[cls._redis_db_number].smembers(cls._name)
                if update.__len__() > 0:
                    update_tuple = ast.literal_eval(str(update).replace('}', '').replace('{', '').replace('b', '').replace("'", ''))
                    if type(update_tuple) is int:
                        update_tuple = (update_tuple,)
                    cls._data.update(update_tuple)
                if cls._data.__len__() > 0:
                    db[cls._redis_db_number].sadd(cls._name, *list(cls._data))
                print('{0}: db={1} set={2}'.format(cls._name, update, cls._data))
        return
