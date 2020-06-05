# -*- coding: utf8 -*-
from main.core.navigator import Navigator
from main.core.db.synchronized.redis.vk.directory_id_dictionary import DirectoryIdDictionary


class Application:
    @classmethod
    def run(cls, message):
        # Ваш функционал вставляется сюда после наследования от данного класса
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
    Показать прииложения, которые находятся в вашей директории с модулем
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
            return True
        else:
            return False
