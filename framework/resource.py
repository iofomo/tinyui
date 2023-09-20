# -*- encoding:utf-8 -*-
# @Brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19
import os

from utils.utils_cmn import CmnUtils
from utils.utils_file import FileUtils

RID_APP_NAME="app-name"
RID_APP_VERSION="app-version"
RID_TEXT_CHOOSE="text-choose"
RID_TEXT_RESET="text-reset"
RID_TEXT_CLEAR="text-clear"
RID_TEXT_CLOSE="text-close"
RID_TEXT_CLEAR_ALL="text-clear-all"
RID_TEXT_DELETE="text-delete"
RID_TEXT_REMOVE="text-remove"
RID_TEXT_ADD="text-add"
RID_TEXT_FINISH="text-finish"
RID_TEXT_START="text-start"
RID_TEXT_STOP="text-stop"
RID_TEXT_SUBMIT="text-submit"
RID_TEXT_SETTING="text-setting"
RID_TEXT_OK="text-ok"
RID_TEXT_CANCEL="text-cancel"
RID_TEXT_REFRESH="text-refresh"
RID_TEXT_EXECUTE="text-execute"
RID_TEXT_SELECT_DELETE="text-select-delete"
RID_TEXT_SELECT_ALL="text-select-all"
RID_TEXT_SELECT_INVERT="text-select-invert"
RID_TEXT_SELECT_CLEAR="text-select-clear"
RID_TEXT_LOGGER_CLEAR="text-logger-clear"
RID_TEXT_LOGGER_SAVE="text-logger-save"
RID_TEXT_UNSUPPORT="text-unsupport"
RID_TEXT_UNKNOWN="text-unknown"
RID_TEXT_INFO="text-info"
RID_TEXT_ERROR="text-error"
RID_TEXT_WARN="text-warn"
RID_TEXT_INPUT="text-input"
# --------------------------------------------------------------------------------------------------------------------
class Resource:
    g_resource = {}
    g_module_resource = {}
    g_res_path = None

    @classmethod
    def init(cls, path):
        cls.g_res_path = path + '/res'
        cls.g_resource = FileUtils.loadJsonByFile(cls.g_res_path + os.sep + cls.__get_name__())

    @classmethod
    def getAppVersion(cls): return Resource.getString(RID_APP_VERSION)

    @classmethod
    def getAppName(cls): return Resource.getString(RID_APP_NAME)

    @classmethod
    def getString(cls, key, default=''):
        if key in cls.g_module_resource: return cls.g_module_resource[key]
        return cls.g_resource[key] if key in cls.g_resource else default

    @classmethod
    def __get_name__(cls):
        return 'resource-cn.json' if CmnUtils.isLanguageCN() else 'resource-en.json'

    @classmethod
    def setModulePath(cls, path):
        cls.g_module_resource = FileUtils.loadJsonByFile(path + os.sep + cls.__get_name__())

    @classmethod
    def getBinFile(cls, name):
        if CmnUtils.isOsWindows():
            f = cls.g_res_path + os.sep + name + '.exe'
            if os.path.isfile(f): return f
        elif CmnUtils.isOsMac():
            f = cls.g_res_path + os.sep + name + '_mac'
            if os.path.isfile(f): return f
        f = cls.g_res_path + os.sep + name
        return f if os.path.isfile(f) else None
