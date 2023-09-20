# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from framework.resource import Resource
from framework.FragmentBase import FragmentBase
from ui.uikit import LayoutItem, UiKit, RadioItem, CheckItem
from utils.utils_cmn import CmnUtils
from utils.utils_logger import LoggerUtils

RID_EDIT_NAME = 'edit-name'
RID_ACTION = 'action'

RID_EDIT_NOTMAL = 'edit-notmal'
RID_EDIT_NOTMAL_HINT = 'edit-notmal-hint'
RID_EDIT_BTN = 'edit-btn'
RID_BTN_SETTING = 'text-setting'
RID_EDIT_PASSWORD = 'edit-password'
RID_EDIT_PASSWORD_HINT = 'edit-password-hint'

RID_RADIO_TITLE = 'radio-title'
RID_RADIO_TYPE_1 = 'radio-type-1'
RID_RADIO_TYPE_2 = 'radio-type-2'

RID_CHECKBOX_TITLE = 'checkbox-title'
RID_CHECKBOX_TYPE_1 = 'checkbox-type-1'
RID_CHECKBOX_TYPE_2 = 'checkbox-type-2'


# --------------------------------------------------------------------------------------------------------------------
def createFragment(module):
    return SampleBasicFragment(module)


class SampleBasicFragment(FragmentBase):
    def __init__(self, module):
        FragmentBase.__init__(self, module)

    def onCreate(self, winRoot):
        FragmentBase.onCreate(self, winRoot)
        self.__initView__()
        self.__initData__()

    def __initView__(self):
        self.editText2 = StringVar()
        self.editName, btn = UiKit.createLabelEditorBtn(self.mWindow, Resource.getString(RID_EDIT_BTN), self.editText2,
                                                        LayoutItem(Resource.getString(RID_BTN_SETTING),
                                                                   lambda s=self, t=RID_BTN_SETTING: s.doAction(t))
                                                        )

        self.editText3 = StringVar()
        UiKit.createLabelEditorPassword(self.mWindow, Resource.getString(RID_EDIT_PASSWORD), self.editText3,
                                        Resource.getString(RID_EDIT_PASSWORD_HINT))

        values = ['item-1', 'item-2', 'item-3']
        self.combox = UiKit.createLabelCombox(self.mWindow, values, Resource.getString('text-label-combox'))

        self.radioType = StringVar()
        rItems = [
            RadioItem(Resource.getString(RID_RADIO_TYPE_1), RID_RADIO_TYPE_1,
                      lambda s=self, t=RID_RADIO_TYPE_1: s.doAction(t)),
            RadioItem(Resource.getString(RID_RADIO_TYPE_2), RID_RADIO_TYPE_2,
                      lambda s=self, t=RID_RADIO_TYPE_2: s.doAction(t)),
        ]
        UiKit.createRadio(self.mWindow, self.radioType, rItems, Resource.getString(RID_RADIO_TITLE), 'h')

        self.checkboxType = StringVar()
        rItems = [
            CheckItem(Resource.getString(RID_CHECKBOX_TYPE_1), RID_CHECKBOX_TYPE_1,
                      lambda s=self, t=RID_CHECKBOX_TYPE_1: s.doAction(t)),
            CheckItem(Resource.getString(RID_CHECKBOX_TYPE_2), RID_CHECKBOX_TYPE_2,
                      lambda s=self, t=RID_CHECKBOX_TYPE_2: s.doAction(t)),
        ]
        UiKit.createCheckButton(self.mWindow, rItems, Resource.getString(RID_CHECKBOX_TITLE), 'h')

        # do gap
        UiKit.createGap(self.mWindow)

        # do action
        rightButtons = [
            LayoutItem(Resource.getString('text-start'), lambda s=self, t=RID_ACTION: s.doAction(t))
        ]
        FragmentBase.createConsoleLayoutButtons(self, rightButtons)

        # results
        self.consoleCreate(self.mWindow)
        self.consoleSetText(Resource.getString('console-info'))

    def __initData__(self):
        val = self.mModule.getCache(RID_EDIT_NAME)
        if not CmnUtils.isEmpty(val): self.editName.set(val)
        val = self.mModule.getCache(RID_RADIO_TITLE)
        self.radioType.set(RID_CHECKBOX_TYPE_1 if CmnUtils.isEmpty(val) else val)

    def saveCache(self):
        self.mModule.setName(self.editName.get())
        self.mModule.setCache(RID_EDIT_NAME, self.editName.get())
        self.mModule.setComboxValue(self.combox.getSelection())
        self.mModule.setRadioValue(self.radioType.get())

    def doAction(self, id):
        FragmentBase.doAction(self, id)
        if id == RID_ACTION:
            self.doAsyncActionCall(SampleBasicFragment.doAsyncAction, self)
        elif id == RID_BTN_SETTING:
            print('has set')

    @staticmethod
    def doAsyncAction(argSelf):
        try:
            argSelf.saveCache()
            argSelf.mModule.doAction()
        except Exception as e:
            LoggerUtils.exception(e)
