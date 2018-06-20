# coding: utf-8
from __future__ import unicode_literals

from natasha.data import load_lines
from yargy.predicates import (dictionary)
DATERELATIVE_DICT = dictionary(set(load_lines('./../dictionaries/null.txt')))
