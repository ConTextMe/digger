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
  from collections import OrderedDict
  import importlib
  from lib.dig_extractors import init, ExportFileClose
  from lib.digestAnnotations import annotateAsDigestXML  
  from lib.func import dumpVar
  extractor = init(args, session)

  fact = {}; annotationSettings = {}
  annotate = 0
  annotationStruct = OrderedDict()
  
  for ex in session['cognitions']: 
    fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    annotationSettings[ex] = fact[ex].annotationSettings()

    for page in sentenceStruct:
      if page not in annotationStruct:
        annotationStruct[page] = OrderedDict()
      if ex not in annotationStruct[page]:
        annotationStruct[page][ex] = OrderedDict()      
        
      if args.debug == 1: dumpVar(page, 'extractM, Page: ')  
      for sentence in sentenceStruct[page]:  
        if sentence == 'par': continue
        else:
          if sentence not in annotationStruct[page][ex]:
            annotationStruct[page][ex][sentence] = []
          mapReversed = {v: k for k, v in sentenceStruct[page][sentence]['map'].items()}
          if args.debug == 1: dumpVar(sentence, 'extractM, Sentence: ')  
          matches = extractor[ex]['ExtractorHandler'](sentenceStruct[page][sentence]['sen'])
          for match in matches:
            #print('fact: ' + str(match.fact) + ', span: ' + str(match.span) + ', map: ' + str(mapReversed))
            spanFitted = "{:0>3.0f}".format(match.span[0])
            if match.span[0] in mapReversed:
              wordStartPos = int(mapReversed[match.span[0]])+1
              annotate = 1
            elif match.span[0]-1 in mapReversed:
              if args.debug == 1: dumpVar(page, 'extractM, annotation symbol lookup fix: -1')  
              wordStartPos = int(mapReversed[match.span[0] - 1])+1
              annotate = 1                  
            else:
              print('Oops, annotation needs some fixes')
              print("### Page: " + str(page) + "', fact : '" + str(match.fact) + ', span: ' + str(match.span) + ', map: ' + str(mapReversed))              
              
              
            #print("Not in struct - Page: " + str(page) + "', fact : '" + str(match.fact) + ', span: ' + str(match.span) + ', map: ' + str(mapReversed))
              
            if annotate == 1:
              annotationStruct[page][ex][sentence].append(wordStartPos)
              annotate = 0

            start, stop = match.span
            fact[ex].elasticExporter(args, session, match, extractor[ex]['FileWriter'], page, sentence)
    
  session['annotationSettings'] = annotationSettings
  annotateAsDigestXML(args, session, sentenceStruct, annotationStruct)
            
  ExportFileClose(extractor, session)      
