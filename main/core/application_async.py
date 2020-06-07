# -*- coding: utf8 -*-

from main.core.application import Application
from main.core.db.synchronized.redis.discord.directory_id_dictionary import DirectoryIdDictionary
from main.core.navigator import Navigator


class AsyncApplication(Application):
    @classmethod
    async def run(cls, message):
        return super().run(message)

    @classmethod
    async def startup(cls, user_id: int):
        return super().startup(user_id)

    @classmethod
    async def pwd(cls) -> str:
        return super().pwd()

    @classmethod
    async def dir(cls) -> list:
        return Navigator.dir(await cls.pwd())

    @classmethod
    async def _directory_set(cls, user_id: int, cd_path: str):
        DirectoryIdDictionary.set(user_id, cd_path)
        await Navigator.get(cd_path).startup(user_id)

    # TODO Придумать, как можно сократить количество одинакового кода. Разница между этим методом и методом Application.cd только в await-ах
    @classmethod
    async def cd(cls, user_id: int, cd_path: str) -> bool:
        if cd_path == '/':
            await cls._directory_set(user_id, '/')
            return True
        if cd_path.endswith('/'):
            cd_path = cd_path[:-1]
        if cd_path == '..':
            user_path = await cls.pwd()
            if (user_path != '/'):
                cd_path = user_path[:user_path.rfind('/')]
                if cd_path == '':
                    cd_path = '/'
                await cls._directory_set(user_id, cd_path)
                return True
            else:
                return False
        if not cd_path.startswith('/'):
            user_path = await cls.pwd()
            if not user_path.endswith('/'):
                user_path += '/'
            user_path += cd_path
            cd_path = user_path
        package_split_point = cd_path.rfind('/')
        if cd_path[package_split_point + 1:] in Navigator.dir(cd_path[:package_split_point]):
            await cls._directory_set(user_id, cd_path)
            return True
        else:
            return False
