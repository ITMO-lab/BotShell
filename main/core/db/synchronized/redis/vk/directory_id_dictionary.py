# -*- coding: utf8 -*-

from main.core.db.synchronized.redis.base.id_dictionary import IdDictionary
import threading


class DirectoryIdDictionary(IdDictionary):
    _data = dict()
    _lock = dict()
    _lock_handle_lock = threading.Lock()
    _name = 'VkDirectoryIdDictionary'
    _redis_db_number = 14
    _redis_lock_db_number = 15
