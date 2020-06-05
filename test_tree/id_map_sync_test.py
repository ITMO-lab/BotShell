# -*- coding: utf8 -*-

from main.core.db.synchronized.redis.directory_id_dictionary import DirectoryIdDictionary

def test1():
    DirectoryIdDictionary.set(1, 'test 1')
    DirectoryIdDictionary.set(2, 'test 2')
    DirectoryIdDictionary.set(3, 'test 3')
    DirectoryIdDictionary.set(4, 'test 4')

    print(DirectoryIdDictionary.get(1))
    print(DirectoryIdDictionary.get(4))
    print(DirectoryIdDictionary.get(111))

    DirectoryIdDictionary.remove(4)
    print(DirectoryIdDictionary.get(4))
    print(DirectoryIdDictionary.remove(4))

    DirectoryIdDictionary.sync()

    DirectoryIdDictionary.set(3, 'test 3 updated')
    DirectoryIdDictionary.set(4, 'test 4 updated')

    DirectoryIdDictionary.sync()

def test2():
    DirectoryIdDictionary.sync()

    DirectoryIdDictionary.set(3, 'test 3 updated TWO')
    DirectoryIdDictionary.set(4, 'test 4 updated TWO')

    DirectoryIdDictionary.sync()
    DirectoryIdDictionary.sync()

"""
Тесты написаны так, что перед ними база данных очищалась
redis-cli -n 14 DEL "YourName"
"""

test2()