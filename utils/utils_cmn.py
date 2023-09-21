# !/usr/bin/framework python
# -*- coding:utf-8 -*-
# @brief:  utils for common
# @date:   2023.08.10 14:40:50

import os, sys, tempfile, subprocess, threading
from utils.utils_logger import LoggerUtils

OS_PLATFORM_LINUX   = 0
OS_PLATFORM_WINDOWS = 1
OS_PLATFORM_MAC     = 2
# -------------------------------------------------------------
class CmnUtils:
    g_os_platform = -1

    @staticmethod
    def isEmpty(s): return s is None or len(s) <= 0

    @classmethod
    def getPlatform(cls):
        if cls.g_os_platform < 0:
            opt = sys.platform.lower()
            if opt.startswith('win'): cls.g_os_platform = OS_PLATFORM_WINDOWS
            elif 'darwin' == opt: cls.g_os_platform = OS_PLATFORM_MAC
            else: cls.g_os_platform = OS_PLATFORM_LINUX
        return cls.g_os_platform

    @staticmethod
    def isOsLinux(): return OS_PLATFORM_LINUX == CmnUtils.getPlatform()

    @staticmethod
    def isOsWindows(): return OS_PLATFORM_WINDOWS == CmnUtils.getPlatform()

    @staticmethod
    def isOsMac(): return OS_PLATFORM_MAC == CmnUtils.getPlatform()

    @staticmethod
    def getOSUserPath(): return os.path.expanduser('~')

    @staticmethod
    def getOsStuffix():
        if CmnUtils.isOsMac(): return '_mac'
        if CmnUtils.isOsWindows(): return '.exe'
        return ''

    @staticmethod
    def formatCmdArg(arg):
        if CmnUtils.isEmpty(arg): return arg
        arg = arg.replace('\\', '/')
        if 0 <= arg.find('*'): return arg
        return '"' + arg + '"'

    @staticmethod
    def doCmd(cmd):
        if CmnUtils.isOsWindows() and cmd.startswith('chmod '): return ''
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            line, l = '', ' '
            while l != '' or p.poll() is None:
                l = p.stdout.readline().decode()
                line += l
            return line
        except Exception as e:
            LoggerUtils.println(e)
        return ''

    @staticmethod
    def doCmd2File(cmd, fname, ignoreEmpty = True):
        if CmnUtils.isOsWindows() and cmd.startswith('chmod '): return ''
        try:
            # print(cmd)
            # ret = subprocess.check_output(cmd, shell=True)
            # return ret.decode()
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            l = ''
            with open(fname, 'w') as f:
                while l != '' or p.poll() is None:
                    l = p.stdout.readline().decode()
                    f.write(l)
            return False
        except Exception as e:
            LoggerUtils.println(e)
        finally:
            if ignoreEmpty and os.path.getsize(fname) <= 0:
                try: os.remove(fname)
                except Exception as e: pass

        return False

    @staticmethod
    def doCmdEx(cmd):
        outResults = ''
        errResults = ''
        if CmnUtils.isOsWindows() and cmd.startswith('chmod '): return outResults, errResults

        try:
            stdoutFile = tempfile.TemporaryFile(mode='w+')
            stderrFile = tempfile.TemporaryFile(mode='w+')
            p = subprocess.Popen(cmd, shell=True, stdout=stdoutFile.fileno(), stderr=stderrFile.fileno())
            p.wait()

            stdoutFile.seek(0)
            outResults = stdoutFile.read()
            stderrFile.seek(0)
            errResults = stderrFile.read()
        except Exception as e:
            if cmd == "aapt": return None, None
            LoggerUtils.println(e)
        finally:
            if stdoutFile: stdoutFile.close()
            if stderrFile: stderrFile.close()
        return outResults, errResults

    @staticmethod
    def doCmdCall(cmd):
        isWin = CmnUtils.isOsWindows()
        if isWin and cmd.startswith('chmod '): return 0
        try:
            # return subprocess.call(cmd, shell=True)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            l = ' '
            while l != '' or p.poll() is None:
                l = p.stdout.readline().decode()
                l = l.strip()
                if isWin:
                    l1 = l.replace('\n', '').replace('\r', '')
                    if len(l1) <=0: continue
                LoggerUtils.println(l)
            return p.returncode
        except Exception as e:
            LoggerUtils.println(e)
        return -100

    @staticmethod
    def isPy2(): return 2 == sys.version_info.major

    @staticmethod
    def isPy3(): return 3 <= sys.version_info.major

    @staticmethod
    def input(a): return input(a) if CmnUtils.isPy3() else raw_input(a)

    @staticmethod
    def printDivideLine(msg):
        print ('----- start: %s ---------------------------------------------------------------------------' % msg)

    @staticmethod
    def ensurePermits(path, ff):
        for f in ff: CmnUtils.ensurePermit(path + os.path.sep + f)

    @staticmethod
    def ensurePermit(fileName):
        if CmnUtils.isOsWindows(): return # do nothing
        if fileName.find('*') < 0 and not os.path.isfile(fileName): return
        CmnUtils.doCmd('chmod 777 ' + CmnUtils.formatCmdArg(fileName))

    @staticmethod
    def joinArgs(args):
        cmd = ''
        for arg in args:
            if 0 < arg.find(' '): cmd += ' "' + arg + '"'
            else: cmd += ' ' + arg
        return cmd

    @staticmethod
    def isRelativePath(f):
        if CmnUtils.isOsWindows():
            return len(f) <= 3 or f[1:2] != ':'
        return not f.startswith('/')

    @staticmethod
    def getHash(v):
        l = len(v)
        if l <= 0: return 0, 0
        f = ord(v[0])|(ord(v[l>>1]) << 6)|(ord(v[l-1]) << 12)|(l << 20)

        h = g = 0
        for i in range(l):
            h = (h << 4) + ord(v[i])
            g = h & 0xf0000000
            h ^= g
            h ^= g >> 24
        return h, f

    @staticmethod
    def runThread(cb, cbArgs, sync=False):
        th = cmn_thread(cb, cbArgs)
        th.start()
        if sync: th.join() # wait finished
        return th

    g_os_lang = None
    @classmethod
    def isLanguageCN(cls):
        if CmnUtils.isEmpty(cls.g_os_lang):
            if CmnUtils.isOsWindows():
                import locale
                cls.g_os_lang = locale.getdefaultlocale()[0] if CmnUtils.isPy2() else locale.getlocale()[0]
            elif CmnUtils.isOsMac():
                output = subprocess.check_output(['defaults', 'read', '-g', 'AppleLocale'])
                cls.g_os_lang = output.decode().strip()
            else:
                output = subprocess.check_output(['echo', '$LANG'])
                cls.g_os_lang = output.decode().strip().split('.')[0]
            cls.g_os_lang = cls.g_os_lang.lower()
        # en_US, zh_CN
        # Chinese Simplified China
        return 0 <= cls.g_os_lang.find('_cn') or 0 <= cls.g_os_lang.find('china')

    @classmethod
    def getLanguageName(cls):
        return 'cn' if CmnUtils.isLanguageCN() else 'en'

    @classmethod
    def isJavaEnvOK(cls):
        ret, err = cls.doCmdEx('java -version')
        print(ret)
        print(err)
        if not cls.isEmpty(ret) and 0 < ret.find(' Runtime Environment '): return True
        if not cls.isEmpty(err) and 0 < err.find(' Runtime Environment '): return True
        return False

    @classmethod
    def parseVersion(cls, ver):
        # 1.0.1.1 -> 1.0.1.2
        # 1.0 -> 1.0.0.1
        items = ver.split('.')
        if CmnUtils.isEmpty(items):
            vn, vc = '1.0.0', 1
        elif len(items) <= 1:# 1
            vn, vc = '%s.0.0' % items[0], 1
        elif len(items) <= 2:# 1.0
            vn, vc = '%s.%s.0' % (items[0], items[1]), 1
        elif len(items) <= 3:# 1.0.0
            vn, vc = '%s.%s.%s' % (items[0], items[1], items[2]), 1
        else:# 1.0.0.101
            vn, vc = '%s.%s.%s' % (items[0], items[1], items[2]), int(items[3])
        return vn, vc

    @classmethod
    def updateVersion(cls, ver):
        vn, vc = cls.parseVersion(ver)
        return '%s.%d' % (vn, vc)

    @staticmethod
    def selectProjects(projects, msg=None):
        index = 0
        for project in projects:
            index += 1
            if index < 10:
                LoggerUtils.i('    %d: %s' % (index, project))
            else:
                LoggerUtils.i('   %d: %s' % (index, project))
        LoggerUtils.i('\r\n  ' + ('choose all: <Enter Key>' if CmnUtils.isEmpty(msg) else msg))

        run = CmnUtils.input('  >>>: ')
        run = run.strip()
        if CmnUtils.isEmpty(run): return projects

        pp = []
        ll = len(projects)
        items = run.split(' ')
        for item in items:
            if CmnUtils.isEmpty(item): continue
            try:
                index = int(item) - 1
            except Exception as e:
                continue
            if 0 <= index < ll:
                pp.append(projects[index])
        return pp


class cmn_thread(threading.Thread):
    def __init__(self, _cb, _cbArgs):
         threading.Thread.__init__(self)
         self.th_cb = _cb
         self.th_args = _cbArgs

    def run(self):
        self.th_cb(self.th_args)

def run():
    pass

if __name__ == "__main__":
    run()
