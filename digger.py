#! /usr/bin/env python3
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

## ## ## ## ## python 3 only ## ## ## ## ## 

### SYS
import sys
import argparse
import shutil
import os
import re
from os import popen
import subprocess
from os.path import expanduser
import datetime
from collections import OrderedDict
###

### LOCAL
from  lib.func import get_runPath
###

### VALS
session = OrderedDict()
isbn = 00000
session['tmp_path'] = '/tmp/digger/'
AnnotationMode = 'multiple'
dirIsTemplate = {"_tmpl"}
currDatetime = datetime.datetime.now()
session['currDatetime'] = currDatetime.strftime("%Y-%m-%dT%H:%M:%S")
ExtractorHandler = {}

actions = ['dig', 'extract', 'clean', 'get', 'generate']
actionsDig = ['all', 'mine', 'by']
actionsMined = ['all','my', 'by']
actionsMinedBy = ['author','scheme','viewpoint', 'date']
actionsGenerate = ['annschema', 'toc']
actionsGet = ['hash', 'isbn']
###

### VARS
os.makedirs(session['tmp_path'], exist_ok=True)
p = argparse.ArgumentParser(description='ConTextMe - Digger')
#REQ
if not sys.argv[1]:
  p.add_argument('--action', dest="action",  choices=actions, type=str, required=True, help='Digger action')
else:
  action = sys.argv[1]
p.add_argument('action2', choices=actions)    
p.add_argument('-c', dest="context",  type=str, required=True, help='Document context')
p.add_argument('-f', dest="fileLoc",  type=str, required=True, help='Filename to dig')
p.add_argument('--repdfreader', dest="repdfreader", type=int, default=0, help='Recreate a pdf_dig pdfreader structure if cached')
p.add_argument('--resentence', dest="resentence", type=int, default=0, help='Recreate a pdf_dig sentence structure if cached')

if action == 'dig':
  print('Woh, digging')  
  p.add_argument('--cognitions', dest="cognitions", type=str, help='Cognitions to dig')
  p.add_argument('--expdf', dest="exPDF", type=int, default=1, help='Export annotations to PDF')
  p.add_argument('--annselftest', dest="annselftest", type=int, default=0, help='Create annotation for reader self-test')

elif action == 'dig' or action == 'extract' :        
  p.add_argument('--exes', dest="exES", type=int, default=1, help='Export annotations to ES')    

elif action == 'extract':    
  print('Hey, extracting')

elif action == 'clean':
  print('Hoy, cleaning')

elif action == 'get':
  p.add_argument('--gettype', dest="gettype",  choices=actionsGet, type=str, required=True, help='Digger get action')
  
  print('Wow, new text')

elif action == 'generate':
  print('Doh, generating')
  p.add_argument('--gentype', dest="gentype",  choices=actionsGenerate, type=str, required=True, help='Digger generate action')
  
  
p.add_argument('--debug', dest="debug",  action='store_true', default=0, help='Document context')

args = p.parse_args()


if action == 'dig':
  if args.cognitions:
    cognitions = args.cognitions.split()
  else:
    cognitions = [x for x in os.listdir(get_runPath() + "/../cognitions/") if x not in dirIsTemplate]
  
session['docFilename'] = str(os.path.getsize(args.fileLoc)) + '.' + os.path.basename(args.fileLoc)
###

if action == 'dig':
  from lib.digPDF import digTextFromPDF, digAnnoFromPDF
  #digTextFromPDF(args,session)
  digAnnoFromPDF(args,session)

elif action == 'extract':
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

elif action == 'clean':
  tmpdir = session['tmp_path'] + "/tmp/"
  os.makedirs(tmpdir, exist_ok=True)
  subprocess.Popen(['cp', args.fileLoc, tmpdir]).wait()
  subprocess.Popen(['pdftk', tmpdir + os.path.basename(args.fileLoc), 'output', tmpdir + os.path.basename(args.fileLoc) + '.unc', 'uncompress']).wait()
  subprocess.Popen(["sed -n '/^\/Annots/!p' " + tmpdir + os.path.basename(args.fileLoc) + '.unc > ' + tmpdir + os.path.basename(args.fileLoc) + '.unoannot'], env={'LANG':'C'}, shell=True).wait()
  subprocess.Popen(["pdftk", tmpdir + os.path.basename(args.fileLoc) + ".unoannot", "output", tmpdir + os.path.basename(args.fileLoc), "compress"]).wait()
  subprocess.Popen(["rm " + tmpdir + os.path.basename(args.fileLoc) + ".*"], shell=True).wait()


elif action == 'get':
  from lib.get import getPDF, getPDFAnnotations
  #print(getPDF(args))
  print(getPDFAnnotations(args, mode="author"))
    
  
elif action == 'generate':
  from lib.digPDF import digTextFromPDF
  from lib.extractFunc import extractAnnSchema
  from os.path import expanduser
  
  sentenceStruct = digTextFromPDF(args,session)
  AnnSchemaFile = str(expanduser("~")) + '/.config/okularpartrc'
  AnnSchemaFileWriter = open(AnnSchemaFile,'w')
  extractAnnSchema(sentenceStruct, AnnSchemaFileWriter)
  AnnSchemaFileWriter.close()
