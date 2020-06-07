# -*- coding: utf8 -*-

import inspect
import sys
import importlib
from os import listdir
from os.path import isdir, isfile, join
import main.home as home_dir


class Navigator:
    GLOBAL_HOME_PATH = 'main.home'
    GLOBAL_PACKAGE_PATH = ''
    @classmethod
    def set_global_package_path(cls, path):
        cls.GLOBAL_PACKAGE_PATH = '.' + path

    GLOBAL_APPLICATION_PATH = "<class 'main.core.application.Application'>"

    @classmethod
    def get(cls, user_path: str):
        if user_path.startswith('/'):
            user_path = user_path[1:]
        classes = cls.dir_classes(user_path)
        for spec_class in classes:
            try:
                target_path = user_path
                if target_path != '':
                    target_path += '/'
                target = cls.get_class(target_path + spec_class)
            except:
                continue
            else:
                return target
        raise Exception('Не найден класс-наследник Application в данной директории\n'
                        + 'Проверьте правильность пути и его содержимое ' +
                        f'{cls.GLOBAL_HOME_PATH.replace(".", "/") + cls.GLOBAL_PACKAGE_PATH.replace(".", "/") + "/" + user_path}')

    @classmethod
    def dir(cls, user_path: str):
        if user_path.startswith('/'):
            user_path = user_path[1:]
        user_path = '{0}{1}/{2}'.format(
            str(home_dir.__path__).replace('_NamespacePath([\'', '').replace('\'])', ''),
            cls.GLOBAL_PACKAGE_PATH.replace(".", "/"), user_path)
        only_pkg = [f for f in listdir(user_path) if isdir(join(user_path, f)) and not f.startswith('__')]
        return only_pkg

    @classmethod
    def dir_classes(cls, user_path: str):
        if user_path.startswith('/'):
            user_path = user_path[1:]
        user_path = '{0}{1}/{2}'.format(
            str(home_dir.__path__).replace('_NamespacePath([\'', '').replace('\'])', ''),
            cls.GLOBAL_PACKAGE_PATH.replace(".", "/"), user_path)
        only_files = [f.replace('.py', '') for f in listdir(user_path) if isfile(join(user_path, f)) and
                      f.endswith('.py')]
        return only_files

    @classmethod
    def get_class(cls, user_path: str):
        user_path = cls.GLOBAL_HOME_PATH + cls.GLOBAL_PACKAGE_PATH + '.' + user_path.replace('/', '.')

        safe_flag = 0

        try:
            import_module = importlib.import_module(user_path)
            clsmembers = inspect.getmembers(sys.modules[user_path], inspect.isclass)
        except Exception as e:
            raise e

        depth = 2
        target = None
        for clsmember in clsmembers:
            childs = clsmember[1].mro()
            if len(childs) > depth and \
                    str(childs[len(childs) - 2]) == cls.GLOBAL_APPLICATION_PATH:
                safe_flag += 1
                target = childs[0]
                depth = len(childs)
        if safe_flag < 1:
            raise Exception('Не пройдён флаг безопасности, проверьте правильность наследования класса {0}'.format(clsmembers))

        return target
