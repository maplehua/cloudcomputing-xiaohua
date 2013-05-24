#!/usr/bin/python
# -*- coding: utf-8 -*-
from core.BaseSearch import DictionarySearch

def expand_keyword(keyword):
    keywords = [keyword]
    dictionary = DictionarySearch()
    trans = dictionary.translate(keyword)
    if len(trans):
        keywords.append(trans)
    return keywords
