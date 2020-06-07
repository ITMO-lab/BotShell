# -*- coding: utf8 -*-

from enum import Enum


class EventType(int, Enum):
    MESSAGE_NEW = 1
    MESSAGE_EDIT = 2
    MESSAGE_DELETE = 3
    REACTION_ADD = 4
    REACTION_REMOVE = 5
