# -*- coding: utf-8 -*-
import requests
from config import TRANSLATOR

def trans(src, service = 'youdao'):
    if service == 'youdao':
        result = yd_trans(src)
    return result

def yd_trans(src):
    service = TRANSLATOR['youdao']
    para = {'type':'data',
        'doctype':'json',
        'version':'1.1',
        'keyfrom':service['username'],
        'key':service['key'],
        'q': src
        }
    r = requests.get(service['endpoint'], params = para)
    return r.json()

if __name__ == '__main__':
    print yd_trans('我的青春不是梦')
