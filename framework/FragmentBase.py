# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

try:
    import thread
except ImportError:
    import _thread as thread
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import tkFont as tkfont
except ImportError:
    from tkinter import font as tkfont

from framework.cacher import Cacher
from framework.resource import Resource
from framework.context import Context
from ui.uikit import UiKit, LayoutItem
from utils.utils_file import FileUtils

RES_IS_LOGGER_SAVE = 'text-logger-save'
RES_IS_LOGGER_CLEAR = 'text-logger-clear'


# --------------------------------------------------------------------------------------------------------------------
class FragmentBase:
    def __init__(self, module):
        self.mModule = module
        self.mWindow = None
        self.mWindowRoot = None
        self.__mConsole = None

    def getPath(self):
        return self.mModule.getPath()

    def getCache(self, key, default=''):
        return Cacher.getValue(key, default)

    def setCache(self, key, val):
        return Cacher.setValue(key, val)

    def getString(self, key, default=''):
        return Resource.getString(key, default)

    def onCreate(self, winRoot):
        self.mWindowRoot = winRoot
        # create left layout
        self.mWindowRoot.pack(fill=BOTH, expand=1)
        self.mWindow = PanedWindow(winRoot, orient=VERTICAL)
        self.createSubTitle()
        UiKit.createGap(self.mWindow, 5)

    def onResume(self):
        Context.setModulePath(self.mModule.getPath())
        self.mWindowRoot.add(self.mWindow)
        Context.getStdIO().setCallback(self.__handleConsoleCallback__)

    def onPause(self):
        self.mWindowRoot.remove(self.mWindow)

    def __handleConsoleCallback__(self, msg):
        if self.__mConsole is None: return
        self.__mConsole.insert(END, msg)
        self.__mConsole.see(END)

    def __console__(self, type):
        if type == RES_IS_LOGGER_CLEAR:
            self.__mConsole.delete(0.0, END)
        elif type == RES_IS_LOGGER_SAVE:
            msg = self.__mConsole.get(0.0, END)
            name = FileUtils.saveLog(Context.getTempPath(), msg)
            print('>>>: ' + name)

    def consoleCreate(self, winRoot, onlyRead=False):
        self.__mConsole = UiKit.createOutputText(winRoot, onlyRead=onlyRead)

    def getConsole(self):
        return self.__mConsole

    def consoleSetText(self, msg):
        self.__console__(RES_IS_LOGGER_CLEAR)
        self.__handleConsoleCallback__(msg + '\n')

    def createConsoleLayoutButtons(self, rightButtons, logBtn=True):
        leftButtons = None if not logBtn else [
            LayoutItem(Resource.getString(RES_IS_LOGGER_CLEAR), lambda s=self, t=RES_IS_LOGGER_CLEAR: s.__console__(t)),
            LayoutItem(Resource.getString(RES_IS_LOGGER_SAVE), lambda s=self, t=RES_IS_LOGGER_SAVE: s.__console__(t))
        ]
        UiKit.createLayoutButtons(self.mWindow, leftButtons, rightButtons)

    def createSubTitle(self, title=None):
        title = title if title is not None else self.mModule.getTitle()
        _font = tkfont.Font(family="Helvetica", size=15, weight="bold")
        UiKit.createLabel(self.mWindow, title, 'left', _font)

    def doAsyncActionCall(self, callback, arg, arg2=None, arg3=None):
        if arg2 is None and arg3 is None:
            thread.start_new_thread(callback, (arg,))
        elif arg2 is not None and arg3 is None:
            thread.start_new_thread(callback, (arg, arg2))
        else:
            thread.start_new_thread(callback, (arg, arg2, arg3))

    def doAction(self, resId):
        pass
