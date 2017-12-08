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

from collections import defaultdict, OrderedDict
import json
import os.path

def digTextFromPDF(args,session):
  
  sentenceStruct = OrderedDict()
  fnameSentence = session['tmp_path'] + session['docFilename'] + '_sentence.json'
  if os.path.isfile(fnameSentence):
    with open(fnameSentence, 'r') as f:
      sentenceStruct = json.load(f, object_pairs_hook=OrderedDict)
  else:
    fnameStruct = session['tmp_path'] + session['docFilename'] + '_pdfreader.json'
    if os.path.isfile(fnameStruct):
      with open(fnameStruct, 'r') as f:
        struct = json.load(f, object_pairs_hook=OrderedDict)
    else:
      import lib.digPDFStemmer_word
      struct = lib.digPDFStemmer_word.getPDFStruct(args)
      dump = json.dumps(struct)
      with open(fnameStruct, 'w') as f:
        f.write(dump)
    import lib.digPDFStemmer_sentence
    intermStruct = OrderedDict()
    intermStruct = lib.digPDFStemmer_sentence.makeIntermStruct(struct)    
    sentenceStruct = lib.digPDFStemmer_sentence.makeSentenceStruct(intermStruct)
    dump = json.dumps(sentenceStruct)
    with open(fnameSentence, 'w') as f:
      f.write(dump)
      print(11111)
  
  if args.annselftest == 1:
    import lib.okularAnnotations
    lib.okularAnnotations.struct_annotate(args,sentenceStruct,session)

  #for page in sentenceStruct:
    #for sentence in sentenceStruct[page]:  
      #if "p" in sentenceStruct[page][sentence]:
        #print(sentenceStruct[page][sentence]["s"])
      
