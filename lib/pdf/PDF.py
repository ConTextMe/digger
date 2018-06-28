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


from collections import OrderedDict
import json
import os.path
import sys

#@profile
def digTextFromPDF(args,session):
  
  sentenceStruct = OrderedDict()
  fnameSentence = session['diggedPath'] + session['srcHash'] + '.json'
  if os.path.isfile(fnameSentence) and args.resentence == 0:
    #with open(fnameSentence, 'r') as f:
      #sentenceStruct = json.load(f, object_pairs_hook=OrderedDict)
      print('Using cached pdfStruct & sentenceStruct')
  else:
    fnameStruct = session['pdfstructPath'] + session['srcHash'] + '.json'
    if os.path.isfile(fnameStruct) and args.repdfreader == 0:
      with open(fnameStruct, 'r') as f:
        struct = json.load(f, object_pairs_hook=OrderedDict)
        print('Using cached pdfStruct')
    else:
      import lib.stemmers.StemWord
      struct = lib.stemmers.StemWord.getPDFStruct(args, session)
      dump = json.dumps(struct, separators=(',',':'))
      with open(fnameStruct, 'w') as f:
        f.write(dump)
    import lib.stemmers.StemSentence
    intermStruct = OrderedDict()
    intermStruct = lib.stemmers.StemSentence.makeIntermStruct(struct)    
    sentenceStruct = lib.stemmers.StemSentence.makeSentenceStruct(intermStruct)
    dump = json.dumps(sentenceStruct, ensure_ascii=False, separators=(',',':')) #indent=1 for readable form
    with open(fnameSentence, 'w') as f:
      f.write(dump)
  
  #if "annselftest" in args and args.annselftest == 1:
    #import lib.digestAnnotations
    #annotationStruct = {}; annotationStruct['color'] = "#0713ff"; annotationStruct['opacity'] = "0.2"
    #lib.digestAnnotations.annotateAsDigestXML(args, session, sentenceStruct, annotationStruct)
   
  #print('Mem:sentenceStruct  ', sys.getsizeof(sentenceStruct)/1024, 'K')   
  
