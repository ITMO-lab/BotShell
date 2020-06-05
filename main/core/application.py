# -*- coding: utf8 -*-
from main.core.navigator import Navigator
from main.core.db.synchronized.redis.vk.directory_id_dictionary import DirectoryIdDictionary


class Application:
    """
    Основной метод, обрабатывающий новые события от пользователя.
    """
    @classmethod
    def run(cls, message):
        return

    """
    Метод, вызываемый при переходе в новое приложение командой cd.
    Следует использовать для подгрузки клавиатуры и базового меню нового окна.
    """
    @classmethod
    def startup(cls, user_id: int):
        return

    """
    Показать текущую дирректорию, где находится этот класс
    Корневой папкой считается project/main/home/
    """
    @classmethod
    def pwd(cls) -> str:
        result = cls.__module__.replace(Navigator.GLOBAL_HOME_PATH, '').replace('.', '/')
        result = result[:result.rfind('/')]
        if result == '':
            result = '/'
        return result

    """
    Показать приложения, которые находятся в вашей директории с модулем. 
    Если вы хотите изменить доступ некоторым пользователям к этой директории, 
    Переопределите метод в вашем пакете, вызовите dir супер класса и измените доступный список директорий.
    """
    @classmethod
    def dir(cls) -> list:
        return Navigator.dir(cls.pwd())

    """
    Переидти к модулю по пути cd_path.
    Если начинается с '/', путь глобальный, можно использовать любую длину и вложеность
    Если начинается с имени модуля, путь локальный, берётся один из модулей в dir().
    Также можно вернуться к предыдущему модулю командой 'cd ..'
    Составные команды не принимаются ввиду отсутствия парсера.
    """
    @classmethod
    def cd(cls, user_id: int, cd_path: str) -> bool:
        if cd_path == '/':
            DirectoryIdDictionary.set(user_id, '/')
            Navigator.get('/').startup(user_id)
            return True
        if cd_path.endswith('/'):
            cd_path = cd_path[:-1]
        if cd_path == '..':
            user_path = cls.pwd()
            if (user_path != '/'):
                cd_path = user_path[:user_path.rfind('/')]
                if cd_path == '':
                    cd_path = '/'
                DirectoryIdDictionary.set(user_id, cd_path)
                Navigator.get(cd_path).startup(user_id)
                return True
            else:
                return False
        if not cd_path.startswith('/'):
            user_path = cls.pwd()
            if not user_path.endswith('/'):
                user_path += '/'
            user_path += cd_path
            cd_path = user_path
        package_split_point = cd_path.rfind('/')
        if cd_path[package_split_point + 1:] in Navigator.dir(cd_path[:package_split_point]):
            DirectoryIdDictionary.set(user_id, cd_path)
            Navigator.get(cd_path).startup(user_id)
            return True
        else:
            return False
