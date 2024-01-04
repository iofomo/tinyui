# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os

try:
    import tkFileDialog
except ImportError:
    from tkinter import filedialog as tkFileDialog
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
try:
    import tkFont as tkfont
except ImportError:
    from tkinter import font as tkfont

from utils.utils_cmn import CmnUtils
from framework.resource import Resource

LIGHT_GRAY = '#d9d9d9'


# ----------------------------------------------------------------------------------------------------------------------
class UiKit:
    @staticmethod
    def createOutputText(winRoot, onlyRead=False):
        win = UiKit.createSubWindow(winRoot, VERTICAL)

        txt = Text(win, highlightcolor=LIGHT_GRAY, highlightbackground=LIGHT_GRAY, background=LIGHT_GRAY, insertbackground=LIGHT_GRAY)
        # if onlyRead: txt.bind('<KeyPress>', lambda e: 'break')
        win.add(txt)
        return txt

    @staticmethod
    def createSubWindow(winRoot, orient=HORIZONTAL):
        win = PanedWindow(winRoot, orient=orient)
        if isinstance(winRoot, Widget) and not isinstance(winRoot, LabelFrame): winRoot.add(win)
        else: win.pack()
        return win

    @staticmethod
    def createLayoutButtons(winRoot, leftButtons, rightButtons):
        if isinstance(winRoot, LabelFrame):
            win = winRoot
        else:
            win = UiKit.createSubWindow(winRoot)

        if leftButtons is not None and 0 < len(leftButtons):
            for leftBtn in leftButtons:
                leftBtn.mLayout = Button(win, text=leftBtn.mLayoutName, command=leftBtn.mLayoutCommand)
                leftBtn.mLayout.pack(side=LEFT)

        if rightButtons is not None and 0 < len(rightButtons):
            for rightBtn in rightButtons:
                rightBtn.mLayout = Button(win, text=rightBtn.mLayoutName, command=rightBtn.mLayoutCommand)
                rightBtn.mLayout.pack(side=RIGHT)

    @staticmethod
    def createLayoutButtonsWithFrame(winRoot, title, leftButtons, rightButtons):
        win = UiKit.createSubWindow(winRoot)
        labelframe = LabelFrame(win, text=title)
        labelframe.pack(fill="both", ipadx=10, padx=10, pady=10, side=LEFT)

        UiKit.createGap(labelframe, 10)
        if leftButtons is not None and 0 < len(leftButtons):
            winSub = UiKit.createSubWindow(labelframe)
            for leftBtn in leftButtons:
                leftBtn.mLayout = Button(winSub, text=leftBtn.mLayoutName, command=leftBtn.mLayoutCommand)
                leftBtn.mLayout.pack(side=LEFT)
        UiKit.createGap(labelframe, 5)
        if rightButtons is not None and 0 < len(rightButtons):
            winSub = UiKit.createSubWindow(labelframe)
            for rightBtn in rightButtons:
                rightBtn.mLayout = Button(winSub, text=rightBtn.mLayoutName, command=rightBtn.mLayoutCommand)
                rightBtn.mLayout.pack(side=LEFT)
        UiKit.createGap(labelframe, 10)

    @staticmethod
    def createLabelEditorPassword(winRoot, txt, valueType=None, hintTxt=None):
        win = UiKit.createSubWindow(winRoot)

        lb = Label(win, text=txt)
        lb.pack(side=LEFT)
        if valueType:
            pwd = Entry(win, show="*", textvariable=valueType)
        else:
            pwd = Entry(win, show="*")
        pwd.pack(side=LEFT)
        if hintTxt:
            lb = Label(win, text=hintTxt, foreground='darkgray')
            lb.pack(side=LEFT)
        return pwd

    @staticmethod
    def createLabel(winRoot, txt, sd='left', _font=None):
        # side='top' or 'bottom' or 'left' or 'right'
        if _font is None:
            _font = tkfont.Font(family="Arial", size=16)

        win = UiKit.createSubWindow(winRoot)
        lb = Label(win, text=txt, font=_font)
        lb.pack(side=sd)

    @staticmethod
    def createLabelEditor(winRoot, txt, valueType=None, hintTxt=None, state="normal"):
        win = UiKit.createSubWindow(winRoot)

        lb = Label(win, text=txt)
        lb.pack(side=LEFT)
        if valueType:
            ed = Entry(win, textvariable=valueType, state=state)
        else:
            ed = Entry(win, state=state)
        ed.pack(side=LEFT)
        if hintTxt:
            lb = Label(win, text=hintTxt, foreground='darkgray')
            lb.pack(side=LEFT)
        return ed

    @staticmethod
    def createButtonEditorLabel(winRoot, buttonItem, valueType=None, txt=None):
        win = UiKit.createSubWindow(winRoot)

        bt = None
        if buttonItem is not None:
            bt = Button(win, text=buttonItem.mLayoutName, command=buttonItem.mLayoutCommand, borderwidth=2)
            bt.config(relief="raised")
            bt.pack(side=LEFT)

        if valueType is not None:
            ed = Entry(win, textvariable=valueType)
        else:
            ed = Entry(win)
        ed.pack(side=LEFT)

        if txt is not None:
            lb = Label(win, text=txt, foreground='gray')
            lb.pack(side=LEFT)

        return ed, bt

    @staticmethod
    def createLabelEditorButton(winRoot, txt, valueType=None, buttonItem=None):
        win = UiKit.createSubWindow(winRoot)

        lb = Label(win, text=txt)
        lb.pack(side=LEFT)

        if valueType is not None:
            ed = Entry(win, textvariable=valueType)
        else:
            ed = Entry(win)
        ed.pack(side=LEFT)

        bt = None
        if buttonItem is not None:
            bt = Button(win, text=buttonItem.mLayoutName, command=buttonItem.mLayoutCommand, borderwidth=2)
            bt.config(relief="raised")
            bt.pack(side=LEFT)

        return ed, bt

    @staticmethod
    def createLabelCombox(winRoot, values, lbTxt=None):
        win = UiKit.createSubWindow(winRoot)

        if lbTxt is not None:
            lb = Label(win, text=lbTxt)
            lb.pack(side=LEFT)

        if CmnUtils.isPy3():
            from tkinter.ttk import Combobox
            combo = Combobox(win)
            # combo.bind("<<ComboboxSelected>>", handle_selection)  # 绑定选择事件的处理函数
            if values is not None:
                combo['values'] = values
                combo.current(0)
            win.add(combo)
            combo.pack(side=LEFT)
            return XCombox(combo)
        else:
            default_option = StringVar()
            default_option.set(values[0])
            menu = OptionMenu(win, default_option, *values)
            win.add(menu)
            menu.pack(side=LEFT)
            return XCombox(menu, default_option)

    @staticmethod
    def createLeftBtn(winRoot, btName):
        win = UiKit.createSubWindow(winRoot)
        bt = Button(win, text=btName)
        bt.pack(side=LEFT)
        return bt

    @staticmethod
    def createText(winRoot, w=128, h=10):
        win = UiKit.createSubWindow(winRoot)
        txt = Text(win, width=w, height=h)
        txt.pack()
        return txt

    @staticmethod
    def createLabelChooser(winRoot, buttonItem, buttonItem2=None):
        win = UiKit.createSubWindow(winRoot)

        btnTxt = buttonItem.mLayoutName
        if CmnUtils.isEmpty(btnTxt) <= 0: btnTxt = Resource.getString('text-choose')
        btn1 = Button(win, text=btnTxt, command=buttonItem.mLayoutCommand)
        btn1.pack(side=LEFT)

        btn2 = None
        if buttonItem2 is not None:
            btn2 = Button(win, text=buttonItem2.mLayoutName, command=buttonItem2.mLayoutCommand)
            btn2.pack(side=LEFT)

        lb = Label(win, text=buttonItem.mLayoutDefaultTxt, foreground='darkgray', justify=LEFT)
        lb.pack(side=LEFT)
        return btn1, btn2, lb

    @staticmethod
    def createRadio(winRoot, rVal, cb, txt1, val1, txt2=None, val2=None, txt3=None, val3=None):
        win = UiKit.createSubWindow(winRoot)
        if txt1 is not None is not None and val1 is not None: Radiobutton(win, text=txt1, variable=rVal, value=val1, command=cb).pack(side=LEFT)
        if txt2 is not None and val2 is not None: Radiobutton(win, text=txt2, variable=rVal, value=val2, command=cb).pack(side=LEFT)
        if txt3 is not None and val3 is not None: Radiobutton(win, text=txt3, variable=rVal, value=val3, command=cb).pack(side=LEFT)

    @staticmethod
    def createRadio(winRoot, type, rItems, lbtxt=None, layout='v'):
        win = UiKit.createSubWindow(winRoot)
        if lbtxt is not None:
            if layout == 'v':
                Label(win, text=lbtxt).pack(anchor=W)
            elif layout == 'h':
                Label(win, text=lbtxt).pack(side=LEFT)
        for item in rItems:
            if layout == 'v':
                Radiobutton(win, text=item.mLabel, variable=type, value=item.mValue, command=item.mCommand).pack(anchor=W)
            elif layout == 'h':
                Radiobutton(win, text=item.mLabel, variable=type, value=item.mValue, command=item.mCommand).pack(side=LEFT)

    @staticmethod
    def createRadioLine(winRoot, title, desc, rItems, type, s=RIGHT):
        Label(winRoot, text=title).pack(side=LEFT)
        if not CmnUtils.isEmpty(desc): Label(winRoot, text=desc, foreground='darkgray').pack(side=LEFT)
        for item in rItems: Radiobutton(winRoot, text=item.mLabel, variable=type, value=item.mValue, command=item.mCommand).pack(side=s)

    @staticmethod
    def createCheckButton(winRoot, items, lbtxt=None, layout='v'):
        win = UiKit.createSubWindow(winRoot)
        if lbtxt is not None:
            if layout == 'v':
                Label(win, text=lbtxt).pack(anchor=W)
            elif layout == 'h':
                Label(win, text=lbtxt).pack(side=LEFT)
        for item in items:
            if layout == 'v':
                Checkbutton(win, text=item.mLabel, variable=item.mChecked, command=item.mCommand).pack(anchor=W)
            elif layout == 'h':
                Checkbutton(win, text=item.mLabel, variable=item.mChecked, command=item.mCommand).pack(side=LEFT)

    @staticmethod
    def createLabelButton(winRoot, labelText, buttonItem):
        win = UiKit.createSubWindow(winRoot)
        Label(win, text=labelText, foreground='darkgray', justify=LEFT).pack(side=LEFT)
        btn = Button(win, text=buttonItem.mLayoutName, command=buttonItem.mLayoutCommand)
        btn.pack(side=RIGHT)
        return btn

    @staticmethod
    def createButtonLabel(winRoot, buttonItem, labelText):
        win = UiKit.createSubWindow(winRoot)
        btn = Button(win, text=buttonItem.mLayoutName, command=buttonItem.mLayoutCommand)
        btn.pack(side=LEFT)
        Label(win, text=labelText, foreground='gray', justify=LEFT).pack(side=LEFT)
        return btn

    @staticmethod
    def createLabelButtons(winRoot, leftButtons, midLabel, rightButtons):
        win = UiKit.createSubWindow(winRoot)
        if leftButtons is not None and 0 < len(leftButtons):
            for leftBtn in leftButtons:
                leftBtn.mLayout = Button(win, text=leftBtn.mLayoutName, command=leftBtn.mLayoutCommand)
                leftBtn.mLayout.pack(side=LEFT)
        lb = Label(win, text=midLabel, justify=LEFT)
        lb.pack(side=LEFT)
        if rightButtons is not None and 0 < len(rightButtons):
            for rightBtn in rightButtons:
                rightBtn.mLayout = Button(win, text=rightBtn.mLayoutName, command=rightBtn.mLayoutCommand)
                rightBtn.mLayout.pack(side=RIGHT)
        return lb

    @staticmethod
    def createGap(winRoot, h=20):
        win = UiKit.createSubWindow(winRoot)
        gapFrame = Frame(win, height=h)
        gapFrame.pack()

    @staticmethod
    def __parseFileName__(name):
        ff = []
        f = ''
        hasTip = False
        for n in name:
            if '{' == n:
                f = ''
                hasTip = True
                continue
            if '}' == n:
                hasTip = False
                if 0 < len(f): ff.append(f)
                f = ''
                continue
            if n == ' ' and not hasTip:
                if 0 < len(f): ff.append(f)
                f = ''
                continue
            f += n
        if 0 < len(f): ff.append(f)
        return ff

    @staticmethod
    def showAskDir(lastPath, pre=None):
        if CmnUtils.isEmpty(lastPath):
            dir = tkFileDialog.askdirectory()
        else:
            dir = tkFileDialog.askdirectory(initialdir=lastPath)
        if CmnUtils.isEmpty(dir): return None
        dir = dir.replace('\\', '/')
        if pre is not None: print(pre)
        print(dir)
        print('\n')
        return dir

    @staticmethod
    def showAskFiles(path, pre=None):
        if CmnUtils.isEmpty(path):
            ff = tkFileDialog.askopenfilenames()
        else:
            ff = tkFileDialog.askopenfilenames(initialdir=path)
        if CmnUtils.isEmpty(ff): return None
        # if type(ff) == unicode: ff = ZUi.__parseFileName__(ff)

        if pre is not None: print(pre)
        realFF = []
        for f in ff:
            f = f.replace('\\', '/')
            if not os.path.isfile(f): continue
            print(f)
            realFF.append(f)
        print('\n')
        return realFF

    @staticmethod
    def showAskFile(path, pre=None):
        if CmnUtils.isEmpty(path):
            f = tkFileDialog.askopenfilename()
        else:
            f = tkFileDialog.askopenfilename(initialdir=path)
        if CmnUtils.isEmpty(f): return None
        f = f.replace('\\', '/')
        if pre is not None: print(pre)
        print(f)
        print('\n')
        return f

    @staticmethod
    def getUiFileName(fileName):
        if CmnUtils.isEmpty(fileName): return ''
        items = fileName.split('/')
        if len(items) <= 3: return fileName
        return '.../' + '/'.join(items[-2:])


class LayoutItem:
    def __init__(self, name, command, defaultTxt=''):
        self.mLayout = None
        self.mLayoutName = name
        self.mLayoutCommand = command
        self.mLayoutDefaultTxt = defaultTxt

    def setTitle(self, txt):
        if self.mLayout is not None: self.mLayout['text'] = txt

    def getTitle(self):
        if self.mLayout is not None: return self.mLayout['text']
        return None


class RadioItem:
    def __init__(self, label, val, command):
        self.mLabel = label
        self.mValue = val
        self.mCommand = command


class CheckItem:
    def __init__(self, label, val, command):
        self.mLabel = label
        self.mValue = val
        self.mChecked = IntVar()
        self.mCommand = command


class XCombox:
    def __init__(self, comp, default_option=None):
        self.default_option = default_option
        self.combox = comp if CmnUtils.isPy3() else None
        self.menu = comp if CmnUtils.isPy2() else None

    def setItems(self, items):
        if self.combox is not None:
            self.combox['values'] = items
            self.combox.current(0)
        elif self.menu is not None:
            self.menu.option_clear()
            for item in items: self.menu.option_add(self.default_option, item)
            self.menu.selection_clear()

    def getSelection(self):
        if self.combox is not None: return self.combox.selection_get()
        if self.default_option is not None: return self.default_option.get()
        return None
