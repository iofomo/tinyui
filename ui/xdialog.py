# -*- encoding:utf-8 -*-
# @Author: ...
# @Date:   2023.08.10 14:40:50

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from utils.utils_cmn import CmnUtils


# ----------------------------------------------------------------------------------------------------------------------
class XDialog:
    def __init__(self):
        self.mWindow = Toplevel()

        screenWidth = self.mWindow.winfo_screenwidth()
        screenHeight = self.mWindow.winfo_screenheight()

        w, h = self.getWindowSize()
        x = int((screenWidth - w) / 2)
        y = int((screenHeight - h) / 2)

        title = self.getTitle()
        if not CmnUtils.isEmpty(title): self.mWindow.title(title)
        self.mWindow.geometry("%sx%s+%s+%s" % (w, h, x, y))
        # The setting window size cannot be changed
        # self.mWindow.resizable(0, 0)

    def getWindowSize(self): return 300, 150
    def getTitle(self): return None

    def onCreateDialog(self):
        self.mWindow.protocol('WM_DELETE_WINDOW', self.mWindow.quit)

    def show(self):
        self.onCreateDialog()
        self.mWindow.focus_set()
        self.mWindow.grab_set()
        self.mWindow.mainloop()
        self.mWindow.destroy()
        return self.getResults()

    def getResults(self): return None

    def doAction(self, id): pass

    def close(self):
        self.mWindow.quit()