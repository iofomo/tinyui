# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

from ui.xdialog import XDialog

try:
    from Tkinter import *
    import tkMessageBox as msgbox
except ImportError as e:
    from tkinter import *
    import tkinter.messagebox as msgbox

from framework.resource import *
from framework.FragmentBase import FragmentBase
from ui.uikit import LayoutItem, UiKit
from utils.utils_cmn import CmnUtils
from utils.utils_logger import LoggerUtils

RID_CHOOSER_FILE = 'chooser-file-button'
RID_CHOOSER_FILES = 'chooser-files-button'
RID_CHOOSER_PATH = 'chooser-path-button'

RID_ACTION = 'action'
RID_BUTTON_INFO = 'text-dialog-info'
RID_BUTTON_CONFIRM = 'text-dialog-confirm'
RID_BUTTON_DEFINE = 'text-dialog-define'
RID_TEXT_TITLE = 'text-dialog-sub-title'
RID_TEXT_HINT = 'text-dialog-sub-hint'
# --------------------------------------------------------------------------------------------------------------------
def createFragment(module):
    return SampleDialogFragment(module)


class SampleDialogFragment(FragmentBase):
    def __init__(self, module):
        FragmentBase.__init__(self, module)

    def onCreate(self, winRoot):
        FragmentBase.onCreate(self, winRoot)
        self.__initView__()
        self.__initData__()

    def __initView__(self):
        _, __, self.lbPath = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString(RID_CHOOSER_PATH),
            lambda s=self, t=RID_CHOOSER_PATH: s.doAction(t),
            Resource.getString('chooser-path-label')
        ))

        _, __, self.lbFile = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString(RID_CHOOSER_FILE),
            lambda s=self, t=RID_CHOOSER_FILE: s.doAction(t),
            Resource.getString('chooser-file-label')
        ))

        _, __, self.lbFiles = UiKit.createLabelChooser(self.mWindow, LayoutItem(
            Resource.getString(RID_CHOOSER_FILES),
            lambda s=self, t=RID_CHOOSER_FILES: s.doAction(t),
            Resource.getString('chooser-files-label')
        ))

        dlgButtons = [
            LayoutItem(Resource.getString(RID_BUTTON_INFO), lambda s=self, t=RID_BUTTON_INFO: s.doAction(t)),
            LayoutItem(Resource.getString(RID_BUTTON_CONFIRM), lambda s=self, t=RID_BUTTON_CONFIRM: s.doAction(t)),
            LayoutItem(Resource.getString(RID_BUTTON_DEFINE), lambda s=self, t=RID_BUTTON_DEFINE: s.doAction(t)),
        ]
        UiKit.createLayoutButtons(self.mWindow, dlgButtons, None)

        # do gap
        UiKit.createGap(self.mWindow)

        # do action
        rightButtons = [
            LayoutItem(Resource.getString(RID_TEXT_START), lambda s=self, t=RID_ACTION: s.doAction(t))
        ]
        FragmentBase.createConsoleLayoutButtons(self, rightButtons)

        # results
        self.consoleCreate(self.mWindow)
        self.consoleSetText(Resource.getString('console-info'))

    def __initData__(self):
        pass

    def saveCache(self):
        pass

    def doAction(self, id):
        FragmentBase.doAction(self, id)
        if id == RID_ACTION:
            self.doAsyncActionCall(SampleDialogFragment.doAsyncAction, self)
        elif id == RID_CHOOSER_FILE:
            ff = UiKit.showAskFile(self.mModule.getCache(id))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setFile(ff)
            self.mModule.setCache(id, ff)
            self.lbFile['text'] = UiKit.getUiFileName(ff)
        elif id == RID_CHOOSER_FILES:
            ff = UiKit.showAskFiles(self.mModule.getCache(id))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setFiles(ff)
            self.mModule.setCache(id, os.path.dirname(ff[0]))
            self.lbFiles['text'] = Resource.getString('label-in-fmt') % (len(ff))
        elif id == RID_CHOOSER_PATH:
            ff = UiKit.showAskDir(self.mModule.getCache(id))
            if CmnUtils.isEmpty(ff): return
            self.mModule.setPath(ff)
            self.mModule.setCache(id, ff)
            self.lbPath['text'] = UiKit.getUiFileName(ff)
        elif id == RID_BUTTON_INFO:
            msgbox.showinfo(Resource.getString(RID_BUTTON_INFO), Resource.getString('text-dialog-info-msg'))
        elif id == RID_BUTTON_CONFIRM:
            msgbox.askokcancel(Resource.getString(RID_BUTTON_CONFIRM), Resource.getString('text-dialog-confirm-msg'))
        elif id == RID_BUTTON_DEFINE:
            SampleSubDialog().show()

    @staticmethod
    def doAsyncAction(argSelf):
        try:
            argSelf.saveCache()
            argSelf.mModule.doAction()
        except Exception as e:
            LoggerUtils.exception(e)


class SampleSubDialog(XDialog):
    def __init__(self):
        XDialog.__init__(self)
        self.mEdit = None
        self.mText = None

    def getTitle(self): return Resource.getString(RID_BUTTON_DEFINE)

    def onCreateDialog(self):
        XDialog.onCreateDialog(self)
        UiKit.createGap(self.mWindow)

        UiKit.createLabel(self.mWindow, Resource.getString(RID_TEXT_TITLE))
        self.mEdit = UiKit.createLabelEditor(self.mWindow, Resource.getString(RID_TEXT_INPUT), Resource.getString(RID_TEXT_HINT))

        UiKit.createGap(self.mWindow)

        rightButtons = [
            LayoutItem(Resource.getString(RID_TEXT_OK), lambda s=self, t=RID_TEXT_OK: s.doAction(t)),
            LayoutItem(Resource.getString(RID_TEXT_CANCEL), lambda s=self, t=RID_TEXT_CANCEL: s.doAction(t))
        ]
        UiKit.createLayoutButtons(self.mWindow, None, rightButtons)

    def doAction(self, id):
        XDialog.doAction(self, id)
        if id == RID_TEXT_OK:
            self.mText = self.mEdit.get()
            print('Got: ' + self.mText)
            self.close()
        if id == RID_TEXT_CANCEL:
            self.close()

    def getResults(self):
        return self.mText