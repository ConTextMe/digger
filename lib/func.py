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
  
def dumpInits(args, session, message):
 print('### ' + message + '.   session: ' + str(session) + ', args:' + str(args)) 

def dumpVar(var, message):
 print('### ' + message + ':' + str(var)) 
