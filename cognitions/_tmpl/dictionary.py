# coding: utf-8
from __future__ import unicode_literals
import re
from  lib.func import get_dictPath, load_regex
from natasha.data import load_lines
from yargy.predicates import (dictionary)

_TMPL_DICT = dictionary(set(load_lines(get_dictPath('_tmpl', 'dict_main.txt'))))
_TMPL_DICT_REGEXP = re.compile(load_regex(get_dictPath('_tmpl', 'dict_main.txt')))
