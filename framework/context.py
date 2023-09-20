# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

import importlib
import os
import sys

from framework.cacher import Cacher
from framework.resource import Resource
from framework.stdio import StdIO
from utils.utils_cmn import CmnUtils
from utils.utils_file import FileUtils
from utils.utils_logger import LoggerUtils


# --------------------------------------------------------------------------------------------------------------------
class Context:
    g_config = {}
    g_root_path = None
    g_env_path = None
    g_tk = None
    g_root_win = None
    g_stdio = None

    @classmethod
    def init(cls, rootPath, envPath):
        cls.g_root_path, cls.g_env_path = rootPath, envPath
        jdata = FileUtils.loadJsonByFile(cls.getConfigFile())
        if jdata is not None: cls.g_config = {}

        Resource.init(rootPath)
        Cacher.init(rootPath)
        FileUtils.ensureDir(Context.getTempPath())
        CmnUtils.doCmd('chmod 0777 ' + Context.getDataPath() + '/*')

    @classmethod
    def getRootPath(cls):
        return cls.g_root_path

    @classmethod
    def getEnvPath(cls):
        return cls.g_env_path

    @classmethod
    def getTempPath(cls):
        return cls.g_root_path + os.sep + 'temp'

    @classmethod
    def getDataPath(cls):
        return cls.g_root_path + os.sep + 'data'

    @classmethod
    def getResPath(cls):
        return cls.g_root_path + os.sep + 'res'

    @classmethod
    def getLogFile(cls):
        return cls.getTempPath() + os.sep + 'log.txt'

    @classmethod
    def getPackageName(cls, fileName):
        return fileName[len(cls.g_root_path) + 1:-3].replace(os.path.sep, '.')

    @classmethod
    def getStdIO(cls):
        if cls.g_stdio is None:
            cls.g_stdio = StdIO()
            sys.stdout = cls.g_stdio
        return cls.g_stdio

    @classmethod
    def getConfig(cls, key, default=''):
        return cls.g_config[key] if cls.g_config is not None and key in cls.g_config else default

    @classmethod
    def setConfig(cls, key, val):
        if key is None or val is None: return False
        if cls.g_config is None: cls.g_config = {}
        cls.g_config[key] = val
        FileUtils.saveJsonToFile(cls.getConfigFile(), cls.g_config)
        return True

    @classmethod
    def removeConfig(cls, key):
        if key is None: return False
        if cls.g_config is None: return True
        if key not in cls.g_config: return True
        del cls.g_config[key]
        FileUtils.saveJsonToFile(cls.getConfigFile(), cls.g_config)
        return True

    @classmethod
    def setModulePath(cls, path):
        Cacher.setModulePath(path)
        Resource.setModulePath(path)

    @classmethod
    def getConfigFile(cls):
        return cls.g_root_path + os.sep + 'res' + os.sep + 'config.json'

    @classmethod
    def setTK(cls, tk):
        cls.g_tk = tk

    @classmethod
    def getTK(cls):
        return cls.g_tk

    @classmethod
    def setRootWindow(cls, val):
        cls.g_root_win = val

    @classmethod
    def getRootWindow(cls):
        return cls.g_root_win

    @classmethod
    def destroy(cls):
        if cls.g_tk is not None:
            try:
                cls.g_tk.destroy()
            except Exception as e:
                print(e)
        FileUtils.remove(Context.getTempPath())

    @classmethod
    def getWinSize(cls):
        return cls.g_tk.winfo_width(), cls.g_tk.winfo_height()

    @staticmethod
    def getModulePaths(path):
        paths = []
        try:
            ff = os.listdir(path)
            for f in ff:
                # print f
                if f.startswith('.'): continue
                fullPath = path + os.path.sep + f + os.path.sep + 'config.json'
                if not os.path.isfile(fullPath): continue
                paths.append(path + os.path.sep + f)
        except Exception as e:
            LoggerUtils.exception(e)

        paths.sort()
        return paths

    @staticmethod
    def __do_create_module_(config, path):
        packName = Context.__parse_pack__(path, config, 'module')
        module = importlib.import_module(packName).createModule(path)
        resource = FileUtils.loadJsonByFile(path + '/resource-' + CmnUtils.getLanguageName() + '.json')
        module.setTitle(resource['title'])
        return module

    @staticmethod
    def createModule(path):
        config = FileUtils.loadJsonByFile(path + '/config.json')
        module = Context.__do_create_module_(config, path)
        packName = Context.__parse_pack__(path, config, 'fragment')
        fragment = importlib.import_module(packName).createFragment(module)
        return module, fragment

    @staticmethod
    def createCommand(typ, path, args):
        config = FileUtils.loadJsonByFile(path + '/config.json')
        packName = Context.__parse_pack__(path, config, 'command')
        command = importlib.import_module(packName).createCommand(typ, path, args)
        if command is None: return None, None
        module = Context.__do_create_module_(config, path)
        command.setModule(module)
        return module, command

    @staticmethod
    def __parse_pack__(path, config, key):
        if key not in config: return None
        fileName = path + os.path.sep + config[key]
        # if not os.path.isfile(fileName): return None
        return Context.getPackageName(fileName)
