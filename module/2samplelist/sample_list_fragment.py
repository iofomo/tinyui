#-*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from framework.resource import *
from framework.FragmentBase import FragmentBase
from ui.uikit import LayoutItem, UiKit
from ui.xlistbox import XListBox
from utils.utils_cmn import CmnUtils
from utils.utils_logger import LoggerUtils

RID_GRID_COLUMN_1 = 'grid-column-1'
RID_GRID_COLUMN_1_HINT = 'grid-column-1-hint'
RID_GRID_COLUMN_2 = 'grid-column-2'
RID_GRID_COLUMN_2_HINT = 'grid-column-4-hint'
RID_GRID_COLUMN_3 = 'grid-column-3'
RID_GRID_COLUMN_3_HINT = 'grid-column-3-hint'


#--------------------------------------------------------------------------------------------------------------------
def createFragment(module):
    return SampleListFragment(module)

class SampleListFragment(FragmentBase):
    def __init__(self, module):
        FragmentBase.__init__(self, module)

    def onCreate(self, winRoot):
        FragmentBase.onCreate(self, winRoot)
        self.__initView__()
        self.__initData__()

    def __initView__(self):
        self.editText1 = StringVar()
        UiKit.createLabelEditor(self.mWindow, Resource.getString(RID_GRID_COLUMN_1), self.editText1, Resource.getString(RID_GRID_COLUMN_1_HINT))

        # do gap
        UiKit.createGap(self.mWindow)

        # do action
        leftButtons = [
            LayoutItem(Resource.getString(RID_TEXT_ADD), lambda s=self, t=RID_TEXT_ADD: s.doAction(t)),
        ]
        UiKit.createLayoutButtons(self.mWindow, leftButtons, None)
        self.listbox = XListBox(self.mWindow)

    def __initData__(self):
        val = self.mModule.getCache(RID_GRID_COLUMN_1, '')
        if not CmnUtils.isEmpty(val): self.editText1.set(val)
        # if not CmnUtils.isEmpty(val): self.editText3.set(val)

    def saveCache(self):
        self.mModule.setCache(RID_GRID_COLUMN_1, self.editText1.get())

    def doAction(self, id):
        FragmentBase.doAction(self, id)
        if id == RID_TEXT_ADD:
            self.listbox.append_item(self.editText1.get())

    @staticmethod
    def doAsyncAction(argSelf):
        try:
            argSelf.saveCache()
            argSelf.mModule.doAction()
        except Exception as e:
            LoggerUtils.exception(e)
