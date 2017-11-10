# coding: utf-8
from __future__ import unicode_literals
import re
from  lib.func import get_dictPath, load_regex
from natasha.data import load_lines
from yargy.predicates import (dictionary)

EDUORGANISATION_DICT = dictionary(set(load_lines(get_dictPath('eduorganisation', 'dict_main.txt'))))
EDUORGANISATION_DICT_REGEXP = re.compile(load_regex(get_dictPath('eduorganisation', 'dict_main.txt')))
