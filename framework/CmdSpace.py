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
from framework.context import Context


# ------------------------------------------------------------------------------------------------------------------------
class CmdSpace:

    def __init__(self):
        self.mModule = None
        self.mCommand = None
        self.mType = None

    def __get_type__(self, args):
        name = '-t'
        l = len(args)
        for i in range(l):
            if args[i] != name: continue
            return args[i + 1] if i + 1 < l else None
        return None

    def __load_module__(self, path, args):
        self.mType = self.__get_type__(args)
        if CmnUtils.isEmpty(self.mType):
            LoggerUtils.e('Not found command for: -t')
            return

        paths = Context.getModulePaths(path)
        for path in paths:
            try:
                self.mModule, self.mCommand = Context.createCommand(self.mType, path, args)
                if self.mCommand is not None: break
            except Exception as e:
                LoggerUtils.exception(e)

    def run(self, args):
        """
        command always contain -t ${type name}, such as:
        python tinyui.py -t basic
        """
        self.__load_module__(Context.getRootPath() + os.sep + 'module', args)
        if self.mCommand is None:
            if self.mType is not None:
                LoggerUtils.e('Not found module for: ' + self.mType)
            return

        try:
            self.mCommand.run()
        except Exception as e:
            print(e)
        finally:
            Context.destroy()
