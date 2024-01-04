#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os
import sys

g_env_path = os.getcwd()
g_this_file = os.path.realpath(sys.argv[0])
g_this_path = os.path.dirname(g_this_file)
sys.path.append(g_this_path)

from utils.utils_import import ImportUtils
from framework.CmdSpace import CmdSpace
from framework.GuiSpace import GuiSpace
from framework.context import Context

ImportUtils.initEnv(g_this_path)

# --------------------------------------------------------------------------------------------------------------------------
def run():
    Context.init(g_this_path, g_env_path)
    if 2 < len(sys.argv):
        CmdSpace().run(sys.argv[1:])
    else:
        GuiSpace().run()


if __name__ == '__main__':
    run()
