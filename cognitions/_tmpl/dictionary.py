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
from natasha.data import load_lines
from yargy.predicates import (dictionary)

_TMPL_DICT = dictionary(set(load_lines(get_dictPath('_tmpl', 'dict_main.txt'))))
_TMPL_DICT_REGEXP = re.compile(load_regex(get_dictPath('_tmpl', 'dict_main.txt')))
