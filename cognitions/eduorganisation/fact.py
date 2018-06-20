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


name = 'eduorganisation'

def fileInit(args, session):
  ExportIndexdata='{"index":{"_index":"' + args.context + '","_type":"' + name + '"}}'
  ExportFile = session['esPath'] + session['contentHash'] + '_' + name + '.json'
  ExportFileWriter = open(ExportFile,'w')
  ExportFileWriter.write(ExportIndexdata + '\n')
  return ExportFileWriter
  
  
def elasticExporter(args, session, match, ExportFileWriter, page, sentence):
    data = {
      #"isbn" : isbn,      
      "page" : page,       
      "sentence" : sentence,       
      "class" : name,
      "orgname" : match.fact.name,
      "tmp" : match.fact.tmp,
      "tmp2" : match.fact.tmp2,
      }
    ExportFileWriter.write(str(data) + '\n')


def annotationSettings():
  extractors = {}; extractors['color'] = "#0713ff"; extractors['opacity'] = "0.2"
  return extractors
