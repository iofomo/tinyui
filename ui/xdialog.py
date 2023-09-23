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
        self.mRoot = Toplevel()

        self.mWindow = PanedWindow(self.mRoot, orient=VERTICAL)
        self.mWindow.pack(fill=BOTH)

        screenWidth = self.mRoot.winfo_screenwidth()
        screenHeight = self.mRoot.winfo_screenheight()

        w, h = self.getWindowSize()
        x = int((screenWidth - w) / 2)
        y = int((screenHeight - h) / 2)

        title = self.getTitle()
        if not CmnUtils.isEmpty(title): self.mRoot.title(title)
        self.mRoot.geometry("%sx%s+%s+%s" % (w, h, x, y))
        # The setting window size cannot be changed
        # self.mWindow.resizable(0, 0)

    def getWindowSize(self): return 300, 150
    def getTitle(self): return None

    def onCreateDialog(self):
        self.mRoot.protocol('WM_DELETE_WINDOW', self.mRoot.quit)

    def show(self):
        self.onCreateDialog()
        self.mRoot.focus_set()
        self.mRoot.grab_set()
        self.mRoot.mainloop()
        self.mRoot.destroy()
        return self.getResults()

    def getResults(self): return None

    def doAction(self, id): pass

    def close(self):
        self.mRoot.quit()