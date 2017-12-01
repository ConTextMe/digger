# coding: utf-8
from __future__ import unicode_literals
from io import open
import os

def get_runPath():
    return os.path.join(os.path.dirname(__file__))

def get_dictPath(cognition, filename):
    return os.path.join(os.path.dirname(__file__) + '/../cognitions/' + cognition, filename)


def maybe_strip_comment(line):
    if '#' in line:
        line = line[:line.index('#')]
        line = line.rstrip()
    return line


def load_regex(filename):
    res = ''
    with open(filename, encoding='utf-8') as file:
        for line in file:
            line = line.rstrip('\n')
            line = maybe_strip_comment(line)
            res = res + line + "|"
    return res[:-1] 
