#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: adb commands for workspace
# @date:   2023.05.10 14:40:50

import os
import sys
import time

from utils.utils_cmn import CmnUtils
from utils.utils_cmn import CmnProcess
from utils.utils_logger import LoggerUtils
from utils.utils_import import ImportUtils
from utils.utils_file import FileUtils
from utils.utils_adb import AdbUtils

ImportUtils.initEnv()

# --------------------------------------------------------------------------------------------------------------------------
def doDumpUi(path, all):
    LoggerUtils.println('dump ui')
    src = '/sdcard/ui.xml'
    ret = AdbUtils.doAdbCmd('shell uiautomator dump ' + src)
    if CmnUtils.isEmpty(ret) or ret.find('xml') <= 0:
        LoggerUtils.error('Error: fail dump ui, ' + ret)
        return
    outFile = path + '/ui.xml'
    AdbUtils.pull(src, outFile)
    if not all: LoggerUtils.println('>>> ' + outFile)

def doDumpLoggerImpl(outFile):
    AdbUtils.doAdbCmd2File('logcat -v threadtime', outFile)

def doDumpLogger(path, all):
    LoggerUtils.println('dump log')

    outFile = path + '/log.txt'
    proc = CmnProcess(doDumpLoggerImpl)
    proc.start(outFile)
    LoggerUtils.println('Wait for 3 seconds ...')
    time.sleep(3)
    proc.terminate()
    if not all: LoggerUtils.println('>>> ' + outFile)

def doDumpScreenShot(path, all):
    LoggerUtils.println('dump screenshot')
    AdbUtils.doAdbCmd('shell screencap -p /sdcard/screenshot.png')
    outFile = path + '/screenshot.png'
    AdbUtils.pull('/sdcard/screenshot.png', outFile)
    if not all: LoggerUtils.println('>>> ' + outFile)

def doDumpProperty(path, all):
    LoggerUtils.println('dump property')
    AdbUtils.doAdbCmd2File('shell getprop', path + '/property.txt')
    if not all: LoggerUtils.println('>>> ' + path + '/property.txt')

def doDumpApps(path, all):
    LoggerUtils.println('dump app list')
    AdbUtils.doAdbCmd2File('shell pm list packages -e', path + '/app-enabled.txt')
    if not all: LoggerUtils.println('>>> ' + path + '/app-enabled.txt')

    AdbUtils.doAdbCmd2File('shell pm list packages -d', path + '/app-disabled.txt')
    if not all: LoggerUtils.println('>>> ' + path + '/app-disabled.txt')

    AdbUtils.doAdbCmd2File('shell pm list packages -3', path + '/app-third.txt')
    if not all: LoggerUtils.println('>>> ' + path + '/app-third.txt')

    AdbUtils.doAdbCmd2File('shell pm list packages -s', path + '/app-system.txt')
    if not all: LoggerUtils.println('>>> ' + path + '/app-system.txt')

def doDumpRuntime(path, all):
    LoggerUtils.println('dump anr')
    outFile = path + '/anr.txt'
    AdbUtils.doAdbCmd2File('pull /data/anr', outFile)
    if not all: LoggerUtils.println('>>> ' + outFile)

    LoggerUtils.println('dump ps')
    outFile = path + '/ps.txt'
    AdbUtils.doAdbCmd2File('shell ps', path + '/ps.txt')
    if not all: LoggerUtils.println('>>> ' + outFile)


def doDumpSys(path):
    os.makedirs(path)
    services = AdbUtils.doAdbCmd('shell dumpsys -l')
    if not CmnUtils.isEmpty(services):
        items = services.split('\n')
        for item in items:
            item = item.strip()
            if CmnUtils.isEmpty(item) or 0 < item.find('/'): continue
            LoggerUtils.println('dump ' + item)
            AdbUtils.doAdbCmd2File('shell dumpsys ' + item, path + '/' + item + '.txt')


def doDumpEnv(path):
    os.makedirs(path)
    LoggerUtils.println('dump net')
    AdbUtils.doAdbCmd2File('shell netcfg', path + '/netcfg.txt')

    LoggerUtils.println('dump property')
    AdbUtils.doAdbCmd2File('shell getprop', path + '/property.txt')

    LoggerUtils.println('dump service')
    AdbUtils.doAdbCmd2File('shell service list', path + '/service.txt')

class ADBDumper:

    def __init__(self, p):
        self.path = CmnUtils.formatArgument(p)

    def collect(self, _mode):
        AdbUtils.ensureEnv()
        outPath = self.path + '/'+ FileUtils.getTempTimeName('dump_')
        try:
            os.makedirs(outPath)
            if CmnUtils.isEmpty(_mode):
                doDumpUi(outPath, True)
                doDumpRuntime(outPath, True)
                doDumpEnv(outPath + '/info')
                doDumpSys(outPath + '/sys')
                doDumpLogger(outPath, True)
                doDumpScreenShot(outPath, True)
                doDumpApps(outPath, True)
            elif 'ui' == _mode:
                doDumpUi(outPath, False)
            elif 'svr' == _mode:
                doDumpSys(outPath + '/sys')
            elif 'log' == _mode:
                doDumpLogger(outPath, False)
            elif 'shot' == _mode:
                doDumpScreenShot(outPath, False)
            elif 'prop' == _mode:
                doDumpProperty(outPath, False)
            elif 'app' == _mode:
                doDumpApps(outPath, False)
            else:
                assert 0, 'Unsupported mode: ' + _mode
            LoggerUtils.println('>>> ' + outPath)
        except Exception as e:
            LoggerUtils.println(e)
