#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os
import sys

g_this_file = os.path.realpath(sys.argv[0])
g_this_path = os.path.dirname(g_this_file)


# --------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    os.system('python "%s/TinyUi.py"' % g_this_path)
