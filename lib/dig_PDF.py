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
import sys

#@profile
def digTextFromPDF(args,session):
  
  sentenceStruct = OrderedDict()
  fnameSentence = session['diggedPath'] + session['srcHash'] + '.json'
  if os.path.isfile(fnameSentence) and args.resentence == 0:
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
      dump = json.dumps(struct, separators=(',',':'))
      with open(fnameStruct, 'w') as f:
        f.write(dump)
    import lib.dig_PDFStemSentence
    intermStruct = OrderedDict()
    intermStruct = lib.dig_PDFStemSentence.makeIntermStruct(struct)    
    sentenceStruct = lib.dig_PDFStemSentence.makeSentenceStruct(intermStruct)
    dump = json.dumps(sentenceStruct, ensure_ascii=False, separators=(',',':')) #indent=1 for readable form
    with open(fnameSentence, 'w') as f:
      f.write(dump)
  
  if "annselftest" in args and args.annselftest == 1:
    import lib.okularAnnotations
    lib.okularAnnotations.struct_annotate(args,sentenceStruct,session)
   
  print('Mem:sentenceStruct  ', sys.getsizeof(sentenceStruct)/1024, 'K')   
  return sentenceStruct
