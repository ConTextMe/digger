# -*- coding: utf-8 -*-
######     ######     ######     ######     ######
##     / / / /    License    \ \ \ \ 
##  ConTextMe copyleft culture, Copyright (C)
##  is prohibited here. This work is licensed 
##  under a CC BY-SA 4.0,
##  Creative Commons Attribution-ShareAlike 4.0,
##  http://creativecommons.org/licenses/by-sa/4.0
######     ######     ######     ######     ######
##    / / / /    Code Climate    \ \ \ \ 
##    Language = python3
##    Indent = space;    2 chars;
######     ######     ######     ######     ######

def init(context, docFilename, cognitions):
  import importlib
  extractor = {}
  
  for ex in cognitions:
    extractor[ex] = {}
    facts = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    grammar = importlib.import_module('cognitions.' + ex.lower() + '.grammar')  
    extractor[ex]['FileWriter'] = facts.fileInit(context, docFilename)
    extractor[ex]['ExtractorHandler'] = eval('grammar.' + ex + 'Extractor')()
  return extractor


def ExportFileClose(extractor, cognitions):
  for ex in cognitions:
    extractor[ex]['FileWriter'].close() 
