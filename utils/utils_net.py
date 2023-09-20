#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief:  utils for network
# @date:   2023.09.10 14:40:50

import os
import sys

from utils.utils_cmn import CmnUtils

try:
    from urllib import request as url_request
except ImportError:
    import urllib2 as url_request


# --------------------------------------------------------------------------------------------------------------------------
def isWindows():
    return 'windows' == sys.platform.lower()


class NetUtils:

    @staticmethod
    def isConnectable(url):
        try:
            res = url_request.urlopen(url)
            return res.getcode() == 200
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def __convert__(s):
        try:
            return s.decode()
        except Exception as e:
            print(e)
            return s

    @staticmethod
    def downloadContentByWeb(url, header=None):
        try:
            if header is None and not isWindows():
                _out, _err = CmnUtils.doCmdEx('curl ' + url)
                if _out is not None: return NetUtils.__convert__(_out)
                print('curl fail')

            nullProxyHandler = url_request.ProxyHandler({})
            opener = url_request.build_opener(nullProxyHandler)
            if header is None:
                opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36')]
            else:
                opener.addheaders = header
            response = opener.open(url)
            return NetUtils.__convert__(response.read())
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def downloadContent(url):
        try:
            if not isWindows():
                _out, _err = CmnUtils.doCmdEx('curl ' + url)
                if _out is not None: return NetUtils.__convert__(_out)
                print('curl fail')

            f = url_request.urlopen(url)
            return NetUtils.__convert__(f.read())
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def downloadFile(url, f):
        if os.path.exists(f): os.remove(f)
        try:
            if not isWindows():
                CmnUtils.doCmdEx('curl ' + url + ' > ' + f)
                if os.path.isfile(f): return True
                print('curl fail')

            net = url_request.urlopen(url)
            with open(f, "wb") as ff: ff.write(net.read())
            return os.path.isfile(f)
        except Exception as e:
            print(e)
        if os.path.exists(f): os.remove(f)
        return False

    @staticmethod
    def downloadFileByWeb(url, f):
        if os.path.exists(f): os.remove(f)
        try:
            nullProxyHandler = url_request.ProxyHandler({})
            opener = url_request.build_opener(nullProxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(url)
            with open(f, "wb") as content: content.write(response.read())
            return os.path.isfile(f)
        except Exception as e:
            print(e)
        if os.path.exists(f): os.remove(f)
        return False
