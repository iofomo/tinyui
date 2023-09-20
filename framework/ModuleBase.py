# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os

from framework.context import Context
from framework.cacher import Cacher
from framework.resource import Resource
from utils.utils_logger import LoggerUtils


# --------------------------------------------------------------------------------------------------------------------
class ModuleBase:
    def __init__(self, path):
        self.__mBasePath = path
        self.__mBaseTitle = ''

    def setTitle(self, v):
        self.__mBaseTitle = v

    def getTitle(self):
        return self.__mBaseTitle

    def getCache(self, key, default=None):
        return Cacher.getValue(key, default)

    def setCache(self, key, val):
        return Cacher.setValue(key, val)

    def getString(self, key, default=''):
        return Resource.getString(key, default)

    def getPath(self):
        return self.__mBasePath

    def isValid(self):
        return False

    def authorChecker(self, msg=None):
        if msg is not None:
            LoggerUtils.println(msg)
            if not msg.startswith('Error: Invalid or corrupt jarfile'): return
        LoggerUtils.e(u'授权失效，请联系管理员获取授权!')

    def doAction(self):
        if not os.path.exists(Context.getTempPath()): os.makedirs(Context.getTempPath())
        return True
