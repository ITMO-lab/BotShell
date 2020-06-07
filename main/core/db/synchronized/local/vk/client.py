# -*- coding: utf8 -*-

import main.core.db.synchronized.local.vk as home_dir

path = str(home_dir.__path__).replace('_NamespacePath([\'', '').replace('\'])', '')
with open(path + '/token.secret') as file:
    token = file.readline()
with open(path + '/confirmation_token.secret') as file:
    confirmation_token = file.readline()
with open(path + '/group_id.secret') as file:
    group_id = file.readline()


class VkClient:
    token = token
    confirmation_token = confirmation_token
    group_id = group_id
    api_url = "https://api.vk.com/method"
    api_version = 5.103
