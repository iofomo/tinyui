# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os

from framework.ModuleBase import ModuleBase
from utils.utils_cmn import CmnUtils


# --------------------------------------------------------------------------------------------------------------------
def createModule(path):
    return SampleListModule(path)


class SampleListModule(ModuleBase):
    def __init__(self, path):
        ModuleBase.__init__(self, path)
        self.mName = None
        self.mInFiles = None

    def setName(self, v):
        if CmnUtils.isEmpty(v): return
        self.mName = v

    def setInputFiles(self, ff):
        self.mInFiles = ff

    def isValid(self):
        if CmnUtils.isEmpty(self.mInFiles):
            print('error: invalid input files !')
            return False
        return True

    def doAction(self):
        ModuleBase.doAction(self)
        if not self.isValid(): return
        print('do check ...')
        for inFile in self.mInFiles:
            inFileName = os.path.basename(inFile)
            CmnUtils.printDivideLine(inFileName)
            print('done.')
