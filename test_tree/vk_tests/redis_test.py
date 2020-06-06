# -*- coding: utf8 -*-

import redis
import time
from main.core.db.redis_app import db


start = time.time()
for i in range(10000):
    db[0].set(str(i), str(i))
print(10000 / (time.time() - start))

start = time.time()
for i in range(10000):
    db[0].get(str(i))
print(10000 / (time.time() - start))