# -*- coding: utf-8 -*-
import requests
from config import TRANSLATE_SERVICE, TRANSLATOR

def trans(src, service = TRANSLATOR):
    if service == 'youdao':
        result = yd_trans(src)
    return result

def yd_trans(src):
    service = TRANSLATE_SERVICE['youdao']
    para = {'type':'data',
        'doctype':'json',
        'version':'1.1',
        'keyfrom':service['username'],
        'key':service['key'],
        'q': src
        }
    r = requests.get(service['endpoint'], params = para).json()['translation']
    if len(r) > 0:
        r = r[0]
    return r

if __name__ == '__main__':
    print yd_trans('我的青春不是梦')
