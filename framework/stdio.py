# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ......
# @Date:   2023.05.15 00:00:19

import os
import sys

try:
    import cStringIO
except ImportError:
    from io import StringIO as cStringIO


# ------------------------------------------------------------------------------------------------------------------------------------
class StdIO:
    def __init__(self):
        self.__content = ''
        self.__callback = None
        self.__orgStdOut = sys.stdout
        self.__memObj, self.__fileObj, self.__nullObj = None, None, None

    def write(self, str):
        # self.__content += str
        if str is None: return
        if self.__callback is None: return
        self.__callback(str)

    def toConsole(self):
        sys.stdout = self.__orgStdOut

    def toMemory(self):
        self.__memObj = cStringIO.StringIO()
        sys.stdout = self.__memObj

    def toFile(self, file='out.txt'):
        self.__fileObj = open(file, 'ab+', 1)
        sys.stdout = self.__fileObj

    def toMete(self):
        self.__nullObj = open(os.devnull, 'wb')
        sys.stdout = self.__nullObj

    def setCallback(self, cb):
        self.__content = ''
        self.__callback = cb
        if cb is not None: sys.stdout = self

    def flush(self): pass

    def reset(self):
        self.__content = ''
        self.__callback = None
        if self.__memObj is not None and not self.__memObj.closed: self.__memObj.close()
        if self.__fileObj is not None and not self.__fileObj.closed: self.__fileObj.close()
        if self.__nullObj is not None and not self.__nullObj.closed: self.__nullObj.close()
        sys.stdout = self.__orgStdOut
