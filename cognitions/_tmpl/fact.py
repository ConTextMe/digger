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


name = '_tmpl'

def fileInit(context, filename):
  ExportIndexdata='{"index":{"_index":"' + context + '","_type":"' + name + '"}}'
  ExportFile = '/tmp/ner/' + filename + '__' + name + '.nlp'
  ExportFileWriter = open(ExportFile,'w')
  ExportFileWriter.write(ExportIndexdata + '\n')
  return ExportFileWriter
  
  
def elasticExporter(match, ExportFileWriter, isbn, page, lineNum):
    data = {
      "isbn" : isbn,      
      "page" : page,       
      "line_abs" : lineNum,       
      "class" : name,
      "name" : match.fact.name,
      }
    ExportFileWriter.write(str(data) + '\n')


def annotationSettings():
  extractors = {}; extractors['color'] = "#000000"; extractors['opacity'] = "0.2"
  return extractors
