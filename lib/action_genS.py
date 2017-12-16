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
  from lib.extract_Annotations import extractAnnSchema
  from os.path import expanduser
  
  sentenceStruct = digTextFromPDF(args,session)
  AnnSchemaFile = str(expanduser("~")) + '/.config/okularpartrc'
  AnnSchemaFileWriter = open(AnnSchemaFile,'w')
  extractAnnSchema(sentenceStruct, AnnSchemaFileWriter)
  AnnSchemaFileWriter.close()
