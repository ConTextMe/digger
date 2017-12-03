#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## ## ## ## ## python 3 only ## ## ## ## ## 

### SYS
import sys
import argparse
import shutil
import os
import re
from os import popen
from os.path import expanduser
import datetime
###

### LOCAL
from  lib.func import get_runPath
###

### VALS
isbn = 00000
AnnotationMode = 'multiple'
dirIsTemplate = {"_tmpl"}
currDatetime = datetime.datetime.now()
currDatetime = currDatetime.strftime("%Y-%m-%dT%H:%M:%S")
ExtractorHandler = {}

actions = ['dig', 'extract', 'clear']
actionsDig = ['all', 'mine', 'by']
actionsMined = ['all','my', 'by']
actionsMinedBy = ['author','scheme','viewpoint', 'date']
###

### VARS

p = argparse.ArgumentParser(description='ConTextMe - Digger')
#REQ
if not sys.argv[1]:
  p.add_argument('--action', dest="action",  choices=actions, type=str, required=True, help='Digger action')
else:
  action = sys.argv[1]
p.add_argument('action2', choices=actions)    
p.add_argument('-c', dest="context",  type=str, required=True, help='Document context')
p.add_argument('-f', dest="fileLoc",  type=str, required=True, help='Filename to dig')

if action == 'dig':
  print('Woh, digging')  
  p.add_argument('--cognitions', dest="cognitions", type=str, help='Cognitions to dig')
  p.add_argument('--expdf', dest="exPDF", type=int, default=1, help='Export annotations to PDF')

elif action == 'dig' or action == 'extract' :        
  p.add_argument('--exes', dest="exES", type=int, default=1, help='Export annotations to ES')    

elif action == 'extract':    
  print('Hey, extracting')
elif action == 'clear':
  print('Hoy, clearing')

p.add_argument('--debug', dest="debug",  action='store_true', default=0, help='Document context')

args = p.parse_args()


if action == 'dig':
  if args.cognitions:
    cognitions = args.cognitions.split()
  else:
    cognitions = [x for x in os.listdir(get_runPath() + "/../cognitions/") if x not in dirIsTemplate]
  
docFilename = str(os.path.getsize(args.fileLoc)) + '.' + os.path.basename(args.fileLoc)
###

if action == 'dig':

  textFileWriter = open('/tmp/ner/' + docFilename + '.txt','w')
  from lib.dig_pdfminer import digTextFromPDF
  digTextFromPDF(args,textFileWriter,currDatetime,docFilename)
  textFileWriter.close()


if action == 'extract':
  from lib.extract import annExtracter
  ### DIR INIT
  popen('mkdir -p /tmp/ner')
  popen('rm /tmp/ner/' + docFilename + '_*.nlp')
  ###  
  
  ### EXTRACTORS
  from lib.extractors import init, ExportFileClose
  extractor = init(args.context, docFilename, cognitions)
  from lib.dig_pdfminer import digUsingNer
  digUsingNer(args, docFilename, extractor, AnnotationMode, AnnotationsFileWriter, currDatetime, isbn, cognitions)
  ExportFileClose(extractor, cognitions)
  ###  
  
  ### FINAL SED
  popen("sed -i 's/None/\"None\"/g' /tmp/ner/*.nlp")
  popen("sed -i 's/\\x27/\"/g' /tmp/ner/*.nlp")
  ###
  
  annExtracter()


### ??
  #### Annotation init
  #from lib.okularAnnotations import annotate
  #AnnotationsFileWriter = open('/tmp/ner/' + docFilename + '.xml','w')
  ####

  #### CLOSE ANNOTATION & MV
  #AnnotationsFileWriter.close()
  ####
