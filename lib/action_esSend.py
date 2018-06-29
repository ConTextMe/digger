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

import os.path
import subprocess

#@profile


def init(args, session):
  for ex in session['cognitions']: 
    esJSON = session['esPath'] + session['srcHash'] + '_' + ex + '.json'
    if os.path.isfile(esJSON) and os.path.getsize(esJSON) > 2:
      subprocess.Popen(['/usr/bin/curl', '-k', '--user',  session['esAuth'], '-XPOST', session['esHost']+"/scv_facts/type/_bulk?pretty", '-H', 'Content-Type: application/x-ndjson', '--data-binary', '@'+esJSON])
