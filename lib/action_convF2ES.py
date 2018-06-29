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
import os

#@profile
def init(args, session):
  if args.debug == 1: print('action_convF2ES')
  for ex in session['cognitions']: 
    factsJSON = session['factsPath'] + session['srcHash'] + '_' + ex + '.json'
    if os.path.isfile(factsJSON) and os.path.getsize(factsJSON) > 2:
      with open(factsJSON, 'r') as f:
        factsStruct = json.load(f, object_pairs_hook=OrderedDict)
        
      esJSON = session['esPath'] + session['srcHash'] + '_' + ex + '.json'
      esJSONWriter = open(esJSON,'w')
  
      for page in factsStruct[ex]:
        for sentence in factsStruct[ex][page]:
          for fact in factsStruct[ex][page][sentence]:
            fact['class'] = ex
            fact['page'] = int(page)
            fact['sentence'] = int(sentence)
            fact['locHash'] = session['srcHash']
            fact['docname'] = session['docname']
            fact['person'] = session['person']            
            esJSONWriter.write('\n{"index": {}}\n')
            esJSONWriter.write(json.dumps(fact, separators=(',',':'), ensure_ascii=False))
            esJSONWriter.write('\n')
            
      esJSONWriter.close()
      if os.path.getsize(esJSON) < 2: 
        os.remove(esJSON)
        
