import json
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'

print(LogLevel.DEBUG)
print(json.dumps(LogLevel.DEBUG))
print(json.loads('"DEBUG"'))
print(LogLevel('DEBUG'))
