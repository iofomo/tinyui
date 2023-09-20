# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os

from framework.ModuleBase import ModuleBase
from utils.utils_cmn import CmnUtils


# --------------------------------------------------------------------------------------------------------------------
def createModule(path):
    return SampleBasicModule(path)


class SampleBasicModule(ModuleBase):
    def __init__(self, path):
        ModuleBase.__init__(self, path)
        self.mName = None
        self.mComboxValue = None
        self.mRadioValue = None

    def setComboxValue(self, v):
        self.mComboxValue = v

    def setRadioValue(self, v):
        self.mRadioValue = None

    def setName(self, v):
        self.mName = v

    def isValid(self):
        if CmnUtils.isEmpty(self.mName):
            print('Error: Invalid edit text !')
            return False
        if CmnUtils.isEmpty(self.mComboxValue):
            print('Error: Invalid combox value !')
            return False
        if CmnUtils.isEmpty(self.mRadioValue):
            print('Error: Invalid radio value !')
            return False
        return True

    def doAction(self):
        ModuleBase.doAction(self)
        if not self.isValid(): return
        # TODO something here ...
        print('done.')
