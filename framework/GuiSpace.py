# - *- encoding:utf-8 -*-
# @Brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from utils.utils_logger import LoggerUtils
from utils.utils_cmn import CmnUtils
from framework.cacher import Cacher
from framework.platform import Platform
from framework.context import Context
from framework.resource import Resource


# ------------------------------------------------------------------------------------------------------------------------
def onDestory():
    try:
        w, h = Context.getWinSize()
        Cacher.setGlobalValue("mainui-width", w)
        Cacher.setGlobalValue("mainui-height", h)
    except Exception as e:
        LoggerUtils.exception(e)
    finally:
        Context.destroy()


class GuiSpace:

    def __init__(self):
        self.mCurIndex = -1
        self.mModules = []
        self.mFragments = []
        self.mWinNote = None
        self.__load_module__(Context.getRootPath() + os.sep + 'module')

    def __load_module__(self, path):
        paths = Context.getModulePaths(path)
        for path in paths:
            try:
                module, fragment = Context.createModule(path)
                self.mModules.append(module)
                self.mFragments.append(fragment)
            except Exception as e:
                LoggerUtils.exception(e)

    def onCreate(self, root):
        # framework
        root.protocol('WM_DELETE_WINDOW', onDestory)

        # main window
        win = PanedWindow(root)
        Context.setRootWindow(win)
        win.pack(fill=BOTH, expand=1)

        # set title
        root.title(Resource.getAppName() + "(v" + Resource.getAppVersion() + ')')

        # set size
        sw, sh = Platform.getScreenSize(root)
        width = Cacher.getGlobalValue("mainui-width")
        height = Cacher.getGlobalValue("mainui-height")
        if width is None or height is None: width, height = 900, 600
        size = '%dx%d+%d+%d' % (width, height, (sw - width) / 2, (sh - height) / 2)
        root.geometry(size)
        root.minsize(width, height)
        # init window frame
        self.__doCreateFrame__(win)

    def __doCreateFrame__(self, winRoot):
        self.__initView__(winRoot)
        self.__initData__()
        self.__initFragment__(winRoot)
        self.__initNote__(winRoot)

    def __initNote__(self, winRoot):
        self.mWinNote = PanedWindow(winRoot, orient=VERTICAL)
        winRoot.add(self.mWinNote)

        txt = Text(self.mWinNote, highlightcolor='white', highlightbackground='white', background='white', insertbackground='white')
        txt.bind('<KeyPress>', lambda e: 'break')
        self.mWinNote.add(txt)

        fname = '/res/note-' + CmnUtils.getLanguageName() + '.txt'
        with open(Context.getRootPath() + fname, 'rb') as f:
            lines = f.readlines()
            for line in lines:
                txt.insert(END, line.decode())

    def __initData__(self):
        self.mListBox.delete(0, self.mListBox.size())
        for index in range(len(self.mModules)):
            self.mListBox.insert(index, self.mModules[index].getTitle())

    def __initFragment__(self, winRoot):
        for index in range(len(self.mFragments)):
            fragment = self.mFragments[index]
            Context.setModulePath(fragment.getPath())
            fragment.onCreate(winRoot)

    def __initView__(self, winRoot):
        # create left layout
        winRoot.pack(fill=BOTH, expand=1)
        win = PanedWindow(winRoot, orient=VERTICAL)
        winRoot.add(win)

        # create list view
        self.mListBox = Listbox(win, bg='white', selectmode=SINGLE, exportselection=False)
        self.mListBox.configure(height=40, font=("Arial", 16))
        self.mListBox.grid(row=1, column=1, padx=(10, 5), pady=10)
        self.mListBox.bind("<<ListboxSelect>>", self.onClick)
        win.add(self.mListBox)

    def onClick(self, *args):
        if self.mListBox.size() <= 0: return
        indexs = self.mListBox.curselection()
        index = int(indexs[0])
        if index == self.mCurIndex: return
        if index < 0 or len(self.mModules) <= index: return
        self.__switchFragment__(self.mCurIndex, index)

    def __switchFragment__(self, indexFrom, indexTo):
        if self.mWinNote is not None:
            Context.getRootWindow().remove(self.mWinNote)
            self.mWinNote = None

        if 0 <= indexFrom < len(self.mFragments):
            self.mFragments[indexFrom].onPause()
        if 0 <= indexTo < len(self.mFragments):
            self.mCurIndex = indexTo
            self.mListBox.see(self.mCurIndex)
            self.mListBox.select_set(self.mCurIndex)
            self.mFragments[self.mCurIndex].onResume()

    def run(self):
        root = Tk()
        try:
            Context.setTK(root)
            self.onCreate(root)
        except Exception as e:
            LoggerUtils.exception(e)
        finally:
            root.mainloop()
