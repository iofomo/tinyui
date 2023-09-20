# -*- encoding:utf-8 -*-
# @brief:  环境安装功能
# @date:   2023.08.25 10:11:19
"""
{
  "1-openpyxl": [
    {
      "type": "dld",
      "from": "http://pan1.xxx.com/f/xxx/?dl=1",
      "to": "setup/temp/openpyxl-2.6.4.tar.gz",
      "msg": "Download openpyxl fail"
    },
    {
      "type": "unzip",
      "from": "setup/temp/openpyxl-2.6.4.tar.gz",
      "to": "setup/temp"
    },
    {
      "type": "install",
      "from": "setup/temp/openpyxl-2.6.4/setup.py"
    }
  ],
  "2-driver": [
    {
      "type": "dld",
      "from": "http://pan1.xxx.com/f/xxx/?dl=1",
      "to": "setup/temp/89.0.4389.23.zip",
      "msg": "Download chrome driver 89.0.4389.23 fail"
    },
    {
      "type": "unzip",
      "from": "setup/temp/89.0.4389.23.zip",
      "to": "data"
    },
    {
      "type": "dld",
      "from": "http://pan1.xxx.com/f/xxx/?dl=1",
      "to": "setup/temp/90.0.4430.24.zip",
      "msg": "Download chrome driver 90.0.4430.24 fail"
    },
    {
      "type": "unzip",
      "from": "setup/temp/90.0.4430.24.zip",
      "to": "data"
    }
  ],
  "3-clear": [
    {
      "type": "rm",
      "from": "setup/temp"
    }
  ],
  "4-check": [
    {
      "type": "cmd",
      "from": "java -version",
      "check": "1.8,1.7",
      "msg": "UNsupport java version !"
    }
  ]
}
"""

import json
import os

from utils.utils_cmn import CmnUtils
from utils.utils_file import FileUtils
from utils.utils_zip import ZipUtils
from utils_net import NetUtils


# ----------------------------------------------------------------------------------------------------------------------
class Setupper:

    def __init__(self, path):
        self.mPath = path

    def setupByJsonFile(self, jfile):
        jdata = FileUtils.loadJsonByFile(jfile)
        if jdata is None:
            print('Setup file fail: ' + jfile)
            return
        self.setupByJsonData(jdata)

    def setupByJsonData(self, jdata):
        keys = jdata.keys()
        keys.sort()
        for k in keys:
            print('setup: ' + k)
            items = jdata[k]
            for item in items:
                typ = item['type']
                msg = item['msg'] if 'msg' in item else None
                if typ == 'dld':
                    self.__doDownload__(item['from'], item['to'], msg)
                elif typ == 'unzip':
                    self.__doUnzip__(item['from'], item['to'], msg)
                elif typ == 'install':
                    self.__doInstall__(item['from'], msg)
                elif typ == 'rm':
                    self.__doRemove__(item['from'], msg)
                elif typ == 'cmd':
                    self.__doExecute__(item['from'], item['check'] if 'check' in item else None, msg)
                else:
                    print('Unknown type: ' + typ)

    # def __doCleanCache__(self):
    #     for root, dirs, files in os.walk(self.mPath):
    #         for dir in dirs:
    #             if dir in tmps:
    #                 dd.append(os.path.join(root, dir))
    #             elif dir.startswith('.'):
    #                 dd.append(os.path.join(root, dir))

    def __doDownload__(self, url, toFile, msg):
        toFile = self.mPath + os.sep + toFile
        FileUtils.ensureFileDir(toFile)
        FileUtils.remove(toFile)
        NetUtils.downloadFile(url, toFile, 1024)
        assert 0 < os.path.getsize(toFile), ('Download fail: ' + url) if msg is None else msg

    def __doUnzip__(self, fromZip, toDir, msg):
        toDir = self.mPath + os.sep + toDir
        fromZip = self.mPath + os.sep + fromZip
        assert os.path.isfile(fromZip), 'Zip file not exist: ' + fromZip
        FileUtils.ensureDir(toDir)
        if not CmnUtils.isOsWindows():
            if fromZip.endswith('.zip'):
                ret = CmnUtils.doCmd('unzip -o %s -d %s/' % (fromZip, toDir))
            else:
                ret = CmnUtils.doCmd('tar zxvf %s -C %s/' % (fromZip, toDir))
            print(ret)
        else:
            ZipUtils.unzip(fromZip, toDir)
        assert os.path.isdir(toDir), ('Unzip fail: ' + fromZip + ' -> ' + toDir) if msg is None else msg

    def __doInstall__(self, pyFile, msg):
        pyFile = self.mPath + os.sep + pyFile
        assert os.path.isfile(pyFile), 'Install file not exist: ' + pyFile
        ret = CmnUtils.doCmd('cd %s && python %s install' % (os.path.dirname(pyFile), os.path.basename(pyFile)))
        assert 0 <= ret or '0' == ret, ('Install fail: ' + pyFile) if msg is None else msg

    def __doRemove__(self, fromDir, msg):
        fromDir = self.mPath + os.sep + fromDir
        FileUtils.remove(fromDir)
        assert not os.path.exists(fromDir), ('Remove fail: ' + fromDir) if msg is None else msg

    def __doExecute__(self, cmd, check, msg):
        cmd = cmd.replace('${path}', self.mPath)
        cmd = cmd.replace('${PATH}', self.mPath)
        print('execute: ' + cmd)
        ret, err = CmnUtils.doCmdEx(cmd)
        print(ret)
        print(err)
        if check is None: return
        items = check.split(',')
        if self.__doCheckResults__(items, ret):
            print('Success')
            return
        if self.__doCheckResults__(items, err):
            print('Success')
            return
        print('Fail' if msg is None else msg)

    def __doCheckResults__(self, items, results):
        for item in items:
            if 0 <= results.find(item): return True
        return False


if __name__ == "__main__":
    jstr = u'''
            {
              "1-openpyxl": [
                {
                  "type": "dld",
                  "from": "http://pan1.xxx.com/f/xxx/?dl=1",
                  "to": "setup/temp/openpyxl-2.6.4.tar.gz",
                  "msg": "Download openpyxl fail"
                },
                {
                  "type": "unzip",
                  "from": "setup/temp/openpyxl-2.6.4.tar.gz",
                  "to": "setup/temp"
                },
                {
                  "type": "install",
                  "from": "setup/temp/openpyxl-2.6.4/setup.py"
                }
              ],
              "2-driver": [
                {
                  "type": "dld",
                  "from": "http://pan1.xxx.com/f/xxx/?dl=1",
                  "to": "setup/temp/89.0.4389.23.zip",
                  "msg": "Download chrome driver 89.0.4389.23 fail"
                },
                {
                  "type": "unzip",
                  "from": "setup/temp/89.0.4389.23.zip",
                  "to": "data"
                },
                {
                  "type": "dld",
                  "from": "http://pan1.xxx.com/f/xxx/?dl=1",
                  "to": "setup/temp/90.0.4430.24.zip",
                  "msg": "Download chrome driver 90.0.4430.24 fail"
                },
                {
                  "type": "unzip",
                  "from": "setup/temp/90.0.4430.24.zip",
                  "to": "data"
                }
              ],
              "3-clear": [
                {
                  "type": "rm",
                  "from": "setup/temp"
                }
              ]
            }
            '''
    s = Setupper('/Users/xxx/workspace/xxx/out/tmp')
    try:
        jdata = json.loads(jstr)
        s.setupByJsonData(jdata)
    except Exception as e:
        print(e)
