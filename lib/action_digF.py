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


#@profile
def init(args, session):
  ### EXTRACTORS
  from collections import OrderedDict
  import importlib
  import sys
  import json
  import os.path
  import gc
  import subprocess
  import lib.ner.extractors
  from lib.func import dumpVar

  factsCached = 0
  for ex in session['cognitions']: 
    factsJSON = session['factsPath'] + session['contentHash'] + '_' + ex + '.json'
    if os.path.isfile(factsJSON) and args.refacts == 0:
      factsCached = factsCached + 1
    else:
      factsCached = -1000
  
  if factsCached > 0:
    print('Using cached for all facts')
  else:
    
    extractor = lib.ner.extractors.init(args, session)
    
    fnameSentence = session['diggedPath'] + session['srcHash'] + '.json'
    if os.path.isfile(fnameSentence):
      with open(fnameSentence, 'r') as f:
        sentenceStruct = json.load(f, object_pairs_hook=OrderedDict)
        
    fact = {}; visualSettings = {}
    annotationStruct = OrderedDict()
    mapWordStruct = OrderedDict()

    for page in sentenceStruct:
      if page not in mapWordStruct:
        mapWordStruct[page] = OrderedDict()
      for sentence in sentenceStruct[page]:  
        if sentence == 'par': continue
        else:
          if sentence not in mapWordStruct[page]:
            mapWordStruct[page][sentence] = OrderedDict()
          for word in sentenceStruct[page][sentence]['pos']:  
            b = sentenceStruct[page][sentence]['pos'][word]['b']
            e = sentenceStruct[page][sentence]['pos'][word]['e']
            wordNumberFitted = "{:0>3.0f}".format(int(word))
            mapWordStruct[page][sentence][b] = OrderedDict()
            mapWordStruct[page][sentence][b] = word
            mapWordStruct[page][sentence][e] = OrderedDict()
            mapWordStruct[page][sentence][e] = word
            #mapWordStruct[page][sentence] = { b : word, e: word }
    
    gc.collect()
    #gc.garbage[0].set_next(None)
    #del gc.garbage[:]

    factData = OrderedDict()
    for ex in session['cognitions']: 
      
      factsJSON = session['factsPath'] + session['contentHash'] + '_' + ex + '.json'
      annotationJSON = session['factsPath'] + session['contentHash'] + '_' + ex + '_anno.json'
      if os.path.isfile(factsJSON) and args.refacts == 0:
          print('Using cached facts for ' + ex)
      else:
        factsJSONWriter = open(factsJSON,'w')
        annotationJSONWriter = open(annotationJSON,'w')
        
        factData[ex] = OrderedDict()
        fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')
        visualSettings[ex] = fact[ex].visualSettings()

        for page in sentenceStruct:
                      
          if args.debug == 1: dumpVar(page, 'extractM, Page: ')  
          for sentence in sentenceStruct[page]:  
            if sentence == 'par': continue
            else:
              
              if args.debug == 1: dumpVar(sentence, 'extractM, Sentence: ')  

              #BUG
              try:
                matches = extractor[ex]['ExtractorHandler'](sentenceStruct[page][sentence]['sen'])
              except TypeError:
                  print('### BUG in extractor in sentence ' + str(sentence) + ', page: ' + str(page) + ', content: ' + str(sentenceStruct[page][sentence]['sen']))    
                  matches = extractor[ex]['ExtractorHandler'](sentenceStruct[page][sentence]['sen'])
              else:
                for match in matches:
                  if match.span[0] in mapWordStruct[page][sentence]:
                    span0 = mapWordStruct[page][sentence][match.span[0]]
                    posSpan0 = match.span[0]
                  else:
                    if match.span[0]+1 in mapWordStruct[page][sentence]: 
                      span0 = mapWordStruct[page][sentence][match.span[0]+1]
                      posSpan0 = match.span[0]+1
                    elif match.span[0]-1 in mapWordStruct[page][sentence]:
                      span0 = mapWordStruct[page][sentence][match.span[0]-1]
                      posSpan0 = match.span[0]-1
                    else:
                      span0 = 0
                    
                  if match.span[1] in mapWordStruct[page][sentence]:
                    span1 = mapWordStruct[page][sentence][match.span[1]]
                    posSpan1 = match.span[1]
                  else:
                    if match.span[1]+1 in mapWordStruct[page][sentence]:
                      span1 = mapWordStruct[page][sentence][match.span[1]+1]
                      posSpan1 = match.span[1]+1
                    elif match.span[1]-1 in mapWordStruct[page][sentence]: 
                      span1 = mapWordStruct[page][sentence][match.span[1]-1]
                      posSpan1 = match.span[1]-1
                    else:
                      span1 = 0

                  if span0 == 0 or span1 == 0:
                    if span0 == 0:
                      b = sentenceStruct[page][sentence]['pos'][span1]['b']
                      e = sentenceStruct[page][sentence]['pos'][span1]['e']
                      if match.span[0] > b and match.span[0] < e:
                        span0 = b
                      else:
                        print('Page: ' + str(page) + ', span: ' + str(match.span) + ', b: ' + str(b) + ', e: ' + str(e))                                    
                        print('### FAIL!! Span0 is not in mapStruct' + ', span: ' + str(match.span) + str(mapWordStruct[page][sentence]))                  
                    elif span1 == 0:
                      b = sentenceStruct[page][sentence]['pos'][span0]['b']
                      e = sentenceStruct[page][sentence]['pos'][span0]['e']
                      if match.span[1] > b and match.span[1] < e:
                        span1 = b
                      else:
                        print('Page: ' + str(page) + ', span: ' + str(match.span) + ', b: ' + str(b) + ', e: ' + str(e))                  
                        print('### FAIL!! Span1 is not in mapStruct' + ', span: ' + str(match.span) + str(mapWordStruct[page][sentence]))                  
                    
                              
                  if int(span0) > 0 and int(span1) > 0:    
                    if span0 == span1:
                      if span0 in sentenceStruct[page][sentence]['pos']:
                          
                          if page not in annotationStruct:
                            annotationStruct[page] = OrderedDict()
                          if ex not in annotationStruct[page]:
                            annotationStruct[page][ex] = OrderedDict()                         
                          if sentence not in annotationStruct[page][ex]:
                            annotationStruct[page][ex][sentence] = []
                            
                          annotationStruct[page][ex][sentence].append(span0)
                      else:
                        print("### FAIL!! span0 algo missed the fact on Page: " + str(page) + "', fact : '" + str(match.fact) + ', span: ' + str(match.span) + ', posSpan0: ' + str(posSpan0)+ ', Span0: ' + str(span0) + ', posSpan1: ' + str(posSpan1) + ', Span1: ' + str(span1))
                    else:
                      for i in range(int(span0), int(span1)+1):
                        i = "{:0>3.0f}".format(int(i))
                        if i in sentenceStruct[page][sentence]['pos']:
                          
                          if page not in annotationStruct:
                            annotationStruct[page] = OrderedDict()
                          if ex not in annotationStruct[page]:
                            annotationStruct[page][ex] = OrderedDict()                         
                          if sentence not in annotationStruct[page][ex]:
                            annotationStruct[page][ex][sentence] = []
                            
                          annotationStruct[page][ex][sentence].append(i)
                        else:
                          print("### FAIL!! range algo missed the fact on Page: " + str(page) + "', fact : '" + str(match.fact) + ', span: ' + str(match.span) + ', i: ' + str(int(span0)+ int(i)) + ', posSpan0: ' + str(posSpan0)+ ', Span0: ' + str(span0) + ', posSpan1: ' + str(posSpan1) + ', Span1: ' + str(span1) + ', i=' + str(i))
                          #print(sentenceStruct[page][sentence]['pos'])
                  start, stop = match.span
                  factResult = fact[ex].factData(args, session, match)
                  if args.debug == 1: dumpVar(factResult, 'fact: ')  
                  if page not in factData[ex]:        
                    factData[ex][page] = OrderedDict()  
                  if sentence not in factData[ex][page]:        
                    factData[ex][page][sentence] = []
                  factData[ex][page][sentence].append(factResult)
                  
        factsJSONWriter.write(json.dumps(factData, separators=(',',':'), ensure_ascii=False))
        factsJSONWriter.close()
        annotationJSONWriter.write(json.dumps(annotationStruct, separators=(',',':'), ensure_ascii=False))
        annotationJSONWriter.close() 

    ###ANNOTATIONS
      #session['visualSettings'] = visualSettings
      #annotateAsDigestXML(args, session, sentenceStruct, annotationStruct)
      #filename = session['prepocessedPath'] + session['contentHash'] + '.pdf'
      #subprocess.Popen(["digest",filename])
      
      #annotateAsDigestQt(args, session)
      
