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

from os import makedirs
import datetime
from collections import OrderedDict

def session():
  session = OrderedDict()
  session['name'] = 'digger'
  
  session['mainPath'] = '/tmp/semantic/'
  makedirs(session['mainPath'], exist_ok=True)
  
  session['srcPath'] = session['mainPath'] + session['name'] + '_file_src/'
  makedirs(session['srcPath'], exist_ok=True)
  
  session['prepocessedPath'] = session['mainPath'] + session['name'] + '_file_prepoc/'
  makedirs(session['prepocessedPath'], exist_ok=True)
  
  session['diggedPath'] = session['mainPath'] + session['name'] + '_struct_step2/'
  makedirs(session['diggedPath'], exist_ok=True)
  
  session['pdfstructPath'] = session['mainPath'] + session['name'] + '_struct_step1/'
  makedirs(session['pdfstructPath'], exist_ok=True)
  
  session['factsPath'] = session['mainPath'] + session['name'] + '_jsons_facts/'
  makedirs(session['factsPath'], exist_ok=True)
  
  session['currDatetime'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
  
  return session

