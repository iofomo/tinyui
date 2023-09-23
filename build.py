#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import os
import shutil
import sys

from utils.utils_cmn import CmnUtils
from utils.utils_file import FileUtils
from utils.utils_logger import LoggerUtils
from utils.utils_zip import ZipUtils

try:
    if sys.version_info.major < 3:  # 2.x
        reload(sys)
        sys.setdefaultencoding('utf8')
    elif 3 == sys.version_info.major and sys.version_info.minor <= 3:  # 3.0 ~ 3.3
        import imp

        imp.reload(sys)
    else:  # 3.4 <=
        import importlib

        importlib.reload(sys)
    import _locale

    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
except Exception as e:
    pass

g_this_file = os.path.realpath(sys.argv[0])
g_this_path = os.path.dirname(g_this_file)

g_root_keep_files = [
    'tinyui.py',
    'tinyui-win.bat',
    'tinyui-mac.command',
    'ReadMe.pdf',
]
g_root_remove_dirs = [
    'doc', 'temp', 'data'
]


# --------------------------------------------------------------------------------------------------------------------------
def mktmp(outPath, appName, vn, vc):
    targetPath = outPath + os.path.sep + ('%s_v%s.%d' % (appName, vn, vc))
    if os.path.isdir(targetPath):
        shutil.rmtree(targetPath)
    if os.path.isdir(targetPath):
        LoggerUtils.error('Fail: clear tmp dir')
        return None, None
    shutil.copytree(g_this_path, targetPath)
    if not os.path.isdir(targetPath):
        LoggerUtils.error('Fail: create tmp dir')
        return None, None
    return targetPath


def doCompile(path):
    l = len(path) + 1
    for dirpath, dirnames, filenames in os.walk(path):
        for dir in dirnames:
            if dir != '__pycache__' and not dir.startswith('.'): continue
            f = os.path.join(dirpath, dir)
            shutil.rmtree(f)
            print('ignore: ' + f)
        for filename in filenames:
            fullName = os.path.join(dirpath, filename)
            if filename.startswith('.') or 0 <= fullName[l:].find('/.'):
                os.remove(fullName)
                continue
            if len(dirpath) <= l: continue
            if filename == 'cache.json' or filename.startswith('.'):
                os.remove(fullName)
                continue
            if filename.endswith('.pyc'):
                os.remove(fullName)
                continue


def doFlush(path, ignoreModules):
    modulePath = path + os.sep + 'module'
    for module in ignoreModules:
        dirPath = modulePath + os.sep + module
        if not os.path.isdir(dirPath): continue
        print('ignore: ' + dirPath)
        shutil.rmtree(dirPath)


def zipIgnoreFilter(targetPath, desZip, filter):
    FileUtils.remove(desZip)
    if filter is None:
        ZipUtils.zipDir(targetPath, desZip)
    else:
        ZipUtils.zipDirWithCallback(targetPath, desZip, filter)
    if os.path.isfile(desZip):
        print(' >>> ' + desZip)
    else:
        LoggerUtils.error('zip fail: ' + desZip)


def doUpdateVerRes(resFile, verString):
    with open(resFile, 'r') as f:
        lines = f.readlines()

    newLines = []
    for line in lines:
        l = line.strip()
        if l.startswith('"app-version"'):
            line = '  "app-version": "%s",\n' % verString
        newLines.append(line)
    with open(resFile, 'w') as f:
        f.writelines(newLines)


def doFlushVersion():
    jdata = FileUtils.loadJsonByFile(g_this_path + os.path.sep + 'res/resource-en.json')
    appVer = jdata['app-version']
    appName = jdata['app-name']

    vn, vc = CmnUtils.parseVersion(appVer)
    vc += 1
    verString = '%s.%d' % (vn, vc)
    doUpdateVerRes(g_this_path + os.path.sep + 'res/resource-en.json', verString)
    doUpdateVerRes(g_this_path + os.path.sep + 'res/resource-cn.json', verString)
    return appName, vn, vc


def getOutputPath():
    if 1 < len(sys.argv): return sys.argv[1]
    return os.path.dirname(g_this_path) + os.sep + 'out'


def getIgnoreModules():
    if 2 < len(sys.argv) and sys.argv[2] == 'all': return []

    modulePath = g_this_path + os.sep + 'module'
    dirs = os.listdir(modulePath)

    modules = []
    for dir in dirs:
        if dir == '__pycache__': continue
        dirPath = modulePath + os.sep + dir
        if not os.path.isdir(dirPath): continue
        modules.append(dir)

    if CmnUtils.isEmpty(modules): return []
    modules.sort()
    mm = CmnUtils.selectProjects(modules)
    return [i for i in modules if i not in mm]


def run():
    outPath = getOutputPath()
    ignoreModules = getIgnoreModules()

    # update version
    appName, vn, vc = doFlushVersion()
    print('Version: %s.%d -> %s.%d' % (vn, vc - 1, vn, vc))

    targetPath = mktmp(outPath, appName, vn, vc)
    if CmnUtils.isEmpty(targetPath): return

    doCompile(targetPath)
    doFlush(targetPath, ignoreModules)

    ff = os.listdir(targetPath)
    for f in ff:
        fullname = targetPath + os.path.sep + f
        if os.path.isfile(fullname):
            if f in g_root_keep_files: continue
            os.remove(fullname)
        elif os.path.isdir(fullname):
            if f not in g_root_remove_dirs: continue
            try:
                shutil.rmtree(fullname)
            except Exception as e:
                pass

    # do zip all
    desZip = targetPath + '.zip'
    zipIgnoreFilter(targetPath, desZip, None)
    FileUtils.remove(targetPath)


if __name__ == "__main__":
    run()
