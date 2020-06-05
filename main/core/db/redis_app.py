# -*- coding: utf8 -*-

import redis

db = [redis.Redis(host='localhost', port=6379, db=it) for it in range(16)]
