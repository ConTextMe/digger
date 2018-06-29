# -*- coding: utf-8 -*-
########    #######    ########    #######    ########    ########
##     / / / /    License    \ \ \ \ 
##    Copyleft culture, Copyright (C) is prohibited here
##    This work is licensed under a CC BY-SA 4.0
##    Creative Commons Attribution-ShareAlike 4.0 License
##    Refer to the http://creativecommons.org/licenses/by-sa/4.0/
########    #######    ########    #######    ########    ########
##    / / / /    Code Climate    \ \ \ \ 
##    Language = python3
##    Indent = space;    2 chars;
########    #######    ########    #######    ########    ########


from __future__ import unicode_literals
import re
from  lib.func import get_dictPath, load_regex
from natasha.data import load_dict
from yargy.predicates import (dictionary)

IN_FIRST = dictionary(set(load_dict('first.txt')))
#FIRST_DICT_REGEXP = re.compile(load_regex('first.txt'))

IN_MAYBE_FIRST = dictionary(set(load_dict('maybe_first.txt')))
#MAYBE_FIRST_DICT_REGEXP = re.compile(load_regex('maybe_first.txt')
                                         
IN_LAST = dictionary(set(load_dict('last.txt')))
#LAST_DICT_REGEXP = re.compile(load_regex('last.txt')
