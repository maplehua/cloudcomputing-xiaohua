#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.BaseSearch import DictionarySearch
from translate import trans

def expand_keyword(keyword):
    keywords = [keyword]
    #dictionary = DictionarySearch()
    #trans = dictionary.translate(keyword)
    results = trans(keyword)
    print results
    if len(results):
        keywords.append(results)
    return keywords

