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

def init(args, session):
  from lib.dig_PDF import digTextFromPDF
  sentenceStruct = digTextFromPDF(args,session)
  extractM(args, session, sentenceStruct)
  
def extractM(args, session, sentenceStruct):
  
  ### EXTRACTORS
  import importlib
  from lib.dig_extractors import init, ExportFileClose
  from lib.func import dumpVar
  extractor = init(args, session)

  fact = {}; annotationSettings = {}
  for ex in session['cognitions']:
    fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    annotationSettings[ex] = fact[ex].annotationSettings()
  ###  
  
  for ex in session['cognitions']:  
    for page in sentenceStruct:
      if args.debug == 1: dumpVar(page, 'extractM, Page: ')  
      for sentence in sentenceStruct[page]:  
        if 'w' in sentenceStruct[page][sentence]: continue
        else:
          if args.debug == 1: dumpVar(sentence, 'extractM, Sentence: ')  
          matches = extractor[ex]['ExtractorHandler'](sentenceStruct[page][sentence]['s'])
          for match in matches:
            start, stop = match.span
            fact[ex].elasticExporter(args, session, match, extractor[ex]['FileWriter'], page, sentence)      
            
  ExportFileClose(extractor, session)      
