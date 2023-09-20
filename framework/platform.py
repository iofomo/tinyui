# -*- encoding:utf-8 -*-
# @Brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import platform
import sys

OS_PLATFORM_LINUX = 0
OS_PLATFORM_WINDOWS = 1
OS_PLATFORM_MAC = 2


# --------------------------------------------------------------------------------------------------------------------
class Platform:
    g_os_platform = -1

    @classmethod
    def getPlatform(cls):
        if cls.g_os_platform < 0:
            opt = sys.platform.lower()
            if 'windows' == opt:
                cls.g_os_platform = OS_PLATFORM_WINDOWS
            elif 'darwin' == opt:
                cls.g_os_platform = OS_PLATFORM_MAC
            else:
                cls.g_os_platform = OS_PLATFORM_LINUX
        return cls.g_os_platform

    @classmethod
    def getPlatformExt(cls):
        if cls.isOsMac(): return "_mac"
        if cls.isOsWindows(): return ".exe"
        return ""

    @classmethod
    def isOS64(cls):
        system, node, release, version, machine, processor = platform.uname()
        return 0 < machine.find('64')

    @staticmethod
    def isOsLinux():
        return OS_PLATFORM_LINUX == Platform.getPlatform()

    @staticmethod
    def isOsWindows():
        return OS_PLATFORM_WINDOWS == Platform.getPlatform()

    @staticmethod
    def isOsMac():
        return OS_PLATFORM_MAC == Platform.getPlatform()

    @staticmethod
    def getScreenSize(root):
        return root.winfo_screenwidth(), root.winfo_screenheight()
