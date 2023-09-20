# -*- encoding:utf-8 -*-
# @Brief:  Storing runtime information in memory
# @Author: ...
# @Date:   2023.05.15 00:00:19

from utils.utils_cmn import CmnUtils
from utils.utils_file import FileUtils


# --------------------------------------------------------------------------------------------------------------------
class Cacher:
    g_module_cacher = {}
    g_module_catcher_file = None

    g_global_cacher = {}
    g_global_cacher_file = None

    g_mem_cacher = {}

    @classmethod
    def init(cls, path):
        cls.g_global_cacher_file = path + '/res/cache.json'
        jdata = FileUtils.loadJsonByFile(cls.g_global_cacher_file)
        if jdata is not None: cls.g_global_cacher = jdata

    @classmethod
    def getMemValue(cls, key):
        return cls.g_mem_cacher[key] if key in cls.g_mem_cacher else None

    @classmethod
    def setMemValue(cls, key, val):
        if CmnUtils.isEmpty(key) or val is None: return False
        cls.g_mem_cacher[key] = val
        return True

    @classmethod
    def getGlobalValue(cls, key):
        return cls.g_global_cacher[key] if key in cls.g_global_cacher else None

    @classmethod
    def setGlobalValue(cls, key, val):
        if CmnUtils.isEmpty(key) or val is None: return False
        cls.g_global_cacher[key] = val
        return FileUtils.saveJsonToFile(cls.g_global_cacher_file, cls.g_global_cacher)

    @classmethod
    def removeGlobalValue(cls, key):
        if CmnUtils.isEmpty(key): return False
        if key not in cls.g_global_cacher: return True
        del cls.g_global_cacher[key]
        return FileUtils.saveJsonToFile(cls.g_global_cacher_file, cls.g_global_cacher)

    # ------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def setModulePath(cls, path):
        cls.g_module_catcher_file = path + '/cache.json'
        jdata = FileUtils.loadJsonByFile(cls.g_module_catcher_file)
        cls.g_module_cacher = jdata if jdata is not None else {}

    @classmethod
    def getValue(cls, key, default=None):
        return cls.g_module_cacher[key] if key in cls.g_module_cacher else default

    @classmethod
    def setValue(cls, key, val):
        if CmnUtils.isEmpty(key) or val is None: return False
        cls.g_module_cacher[key] = val
        return FileUtils.saveJsonToFile(cls.g_module_catcher_file, cls.g_module_cacher)

    @classmethod
    def removeValue(cls, key):
        if CmnUtils.isEmpty(key): return False
        if key not in cls.g_module_cacher: return True
        del cls.g_module_cacher[key]
        return FileUtils.saveJsonToFile(cls.g_module_catcher_file, cls.g_module_cacher)
