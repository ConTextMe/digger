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

PERSON_DICT = dictionary(set(load_dict(get_dictPath('person', 'dict_main.txt'))))
PERSON_DICT_REGEXP = re.compile(load_regex(get_dictPath('person', 'dict_main.txt')))
