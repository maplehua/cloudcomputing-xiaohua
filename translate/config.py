# -*- coding: utf-8 -*-

def yd_trans(src):
    para = {'type':'data',
            'doctype':'json',
            'version':'1.1',
            'keyfrom':keyfrom,
            'key':apikey,
            'q': src
            }
    r = requests.get(url, params = para)
    return r.json()

print trans('我的青春不是梦')
