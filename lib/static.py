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
  session['mainPath'] = '/tmp/' + session['name'] + '/'
  makedirs(session['mainPath'], exist_ok=True)
  session['srcPath'] = session['mainPath'] + 'src/'
  makedirs(session['srcPath'], exist_ok=True)
  session['prepocessedPath'] = session['mainPath'] + 'prepocessed/'
  makedirs(session['prepocessedPath'], exist_ok=True)
  session['diggedPath'] = session['mainPath'] + 'digged/'
  makedirs(session['diggedPath'], exist_ok=True)
  session['pdfstructPath'] = session['mainPath'] + 'pdfstructs/'
  makedirs(session['pdfstructPath'], exist_ok=True)
  session['esPath'] = session['mainPath'] + 'es_json/'
  makedirs(session['esPath'], exist_ok=True)
  session['currDatetime'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
  return session

