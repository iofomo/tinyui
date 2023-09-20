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
    CmnUtils.doCmd('rm -rf ' + targetPath)
    if os.path.isdir(targetPath):
        LoggerUtils.error('Fail: clear tmp dir')
        return None, None
    CmnUtils.doCmdEx('cp -rf ' + g_this_path + ' ' + targetPath)
    if not os.path.isdir(targetPath):
        LoggerUtils.error('Fail: create tmp dir')
        return None, None
    return targetPath


def doCompile(path):
    l = len(path) + 1
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath[l:].startswith('.'):
            CmnUtils.doCmd('rm -rf ' + dirpath)
            continue
        for filename in filenames:
            fullName = os.path.join(dirpath, filename)
            if filename.startswith('.') or 0 <= fullName[l:].find('/.'):
                os.remove(fullName)
                continue
            if len(dirpath) <= l: continue
            if filename == '__init__.py': continue
            if filename == 'setup.py': continue
            if filename == 'setup.pyc':
                os.remove(fullName)
                continue
            if filename.endswith('.py'):
                CmnUtils.doCmd('python -m py_compile ' + fullName)
                os.remove(fullName)
                continue


def doFlush(path):
    CmnUtils.doCmd('rm -f %s/*/*/cache.json' % (path))


def zipXxxCallbackIgnoreFiles(fileName, shortFileName):
    if 0 <= fileName.find('__MACOSX'): return True
    return False


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


def run():
    outPath, buildType = sys.argv[1], sys.argv[2]

    # update version
    appName, vn, vc = doFlushVersion()
    print('version: %s, %d -> %d' % (vn, vc - 1, vc))

    targetPath = mktmp(outPath, appName, vn, vc)
    if CmnUtils.isEmpty(targetPath): return

    CmnUtils.doCmd('cd %s && find . -name "*.pyc" |xargs rm' % g_this_path)
    doCompile(targetPath)
    doFlush(targetPath)

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
