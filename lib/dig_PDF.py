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

from collections import OrderedDict
import json
import os.path

def digTextFromPDF(args,session):
  
  sentenceStruct = OrderedDict()
  fnameSentence = session['diggedPath'] + session['srcHash'] + '.json'
  if os.path.isfile(fnameSentence):
    with open(fnameSentence, 'r') as f:
      sentenceStruct = json.load(f, object_pairs_hook=OrderedDict)
  else:
    fnameStruct = session['pdfstructPath'] + session['srcHash'] + '.json'
    if os.path.isfile(fnameStruct):
      with open(fnameStruct, 'r') as f:
        struct = json.load(f, object_pairs_hook=OrderedDict)
    else:
      import lib.dig_PDFStemWord
      struct = lib.dig_PDFStemWord.getPDFStruct(args, session)
      dump = json.dumps(struct)
      with open(fnameStruct, 'w') as f:
        f.write(dump)
    import lib.dig_PDFStemSentence
    intermStruct = OrderedDict()
    intermStruct = lib.dig_PDFStemSentence.makeIntermStruct(struct)    
    sentenceStruct = lib.dig_PDFStemSentence.makeSentenceStruct(intermStruct)
    dump = json.dumps(sentenceStruct, indent=1, ensure_ascii=False)
    with open(fnameSentence, 'w') as f:
      f.write(dump)
  
  if "annselftest" in args and args.annselftest == 1:
    import lib.okularAnnotations
    lib.okularAnnotations.struct_annotate(args,sentenceStruct,session)
    
  return sentenceStruct
