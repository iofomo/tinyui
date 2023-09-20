# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

from utils.utils_logger import LoggerUtils


# --------------------------------------------------------------------------------------------------------------------
class CommandBase:
    def __init__(self, path, args):
        self.mPath = path
        self.mArgs = args

    def setModule(self, module):
        self.mModule = module

    def getPath(self):
        return self.mModule.getPath()

    def getArgumentByIndex(self, index):
        return None if self.mArgs is None or len(self.mArgs) <= index else self.mArgs[index]

    def getArgumentByName(self, name):
        name = '-' + name
        for i in range(len(self.mArgs)):
            if 0 != (i % 2): continue
            if self.mArgs[i] != name: continue
            return self.mArgs[i+1]
        return None

    def run(self):
        return True
