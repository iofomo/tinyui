# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os

from framework.ModuleBase import ModuleBase
from utils.utils_cmn import CmnUtils


# --------------------------------------------------------------------------------------------------------------------
def createModule(path):
    return SampleDialogModule(path)


class SampleDialogModule(ModuleBase):
    def __init__(self, path):
        ModuleBase.__init__(self, path)
        self.mFile = None
        self.mFiles = None
        self.mPath = None

    def setFile(self, ff):
        self.mFile = ff

    def setFiles(self, ff):
        self.mFiles = ff

    def setPath(self, ff):
        self.mPath = ff

    def isValid(self):
        if CmnUtils.isEmpty(self.mFile):
            print('Error: Invalid file !')
            return False
        if CmnUtils.isEmpty(self.mFiles):
            print('Error: Invalid files !')
            return False
        if CmnUtils.isEmpty(self.mPath):
            print('Error: Invalid path !')
            return False
        return True

    def doAction(self):
        ModuleBase.doAction(self)
        if not self.isValid(): return
        print('do check ...')
        # do something here ...
        for f in self.mFiles:
            inFileName = os.path.basename(f)
            CmnUtils.printDivideLine(inFileName)
        print('done.')
