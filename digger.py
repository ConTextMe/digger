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
import datetime
import importlib
import hashlib
from os import listdir, path, makedirs
from collections import OrderedDict
###

### LOCAL
from  lib.func import get_runPath, dumpInits
###

### VALS
session = OrderedDict()
session['name'] = 'digger'
session['mainPath'] = '/tmp/' + session['name'] + '/'
makedirs(session['mainPath'], exist_ok=True)
session['srcPath'] = session['mainPath'] + 'src/'
makedirs(session['srcPath'], exist_ok=True)
session['prepocessedPath'] = session['mainPath'] + 'prepocessed/'
makedirs(session['prepocessedPath'], exist_ok=True)
session['diggedPath'] = session['mainPath'] + 'digged/'
makedirs(session['diggedPath'], exist_ok=True)
session['pdfstructPath'] = session['mainPath'] + 'pdfstructs/'
makedirs(session['pdfstructPath'], exist_ok=True)
session['esPath'] = session['mainPath'] + 'es_json/'
makedirs(session['esPath'], exist_ok=True)

dirIsTemplate = {"_tmpl"}

actions = ['genS', 'getM', 'getH', 'calls']

actionsMined = ['all','my', 'by']
actionsMinedBy = ['author','scheme','viewpoint', 'date']
actionsGenerate = ['annschema', 'toc']
actionsGet = ['hash', 'isbn']
###

### Vars
session['currDatetime'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
###

### Pre-Actions
p = argparse.ArgumentParser(description='ConTextMe - Digger')
###

### Argument constructor
if not sys.argv[1]:
  p.add_argument('--action', dest="action", type=str, required=True, help='Digger action', choices=actions)
else:
  action = sys.argv[1]
p.add_argument('action', choices=actions)    
p.add_argument('-s', dest="src",  type=str, required=True, help='Source to dig')
p.add_argument('-c', dest="context", type=str, required=True, help='Document context')
p.add_argument('--debug', dest="debug",  action='store_true', default=0, help='Debug mode')
args = p.parse_known_args()[0]
session['srcHash'] = hashlib.sha1(args.src.encode('utf-8')).hexdigest()
### Source choose

if path.isfile(args.src) and args.src.endswith('.pdf'):
  session['preAction'] = 'cp'  
  session['srcType'] = 'file'
  session['docFilename'] = path.basename(args.src)
  
elif path.isfile(args.src) and (args.src.endswith('.doc') or args.src.endswith('.docx')):
  session['preAction'] = 'genPDF'
  session['srcType'] = 'file'
  session['docFilename'] = path.basename(args.src)  
else:
  from urllib.parse import urlparse
  url = urlparse(args.src)
  if (url.scheme == 'http' or url.scheme == 'https') and len(url.netloc) > 1 and url.path.endswith('.pdf'):
    session['preAction'] = 'download'
    session['srcType'] = 'url'
    session['docFilename'] = path.basename(url.path)
    
  elif (url.scheme == 'http' or url.scheme == 'https') and len(url.netloc) > 1:
    session['preAction'] = 'genPDF'
    session['srcType'] = 'url'
    
  elif args.src == 'telegram':
    print('Boilerplate for' + args.src)
  ##
if 'preAction' in session:
  from  lib.preaction import preaction
  if args.debug == 1: dumpInits(args, session, '### before preAction')  
  preaction(args, session)
  if args.debug == 1: dumpInits(args, session, '### after preAction')  

### Action-dependent args
if args.action == 'getM' or args.action == 'getH':
  p.add_argument('--repdfreader', dest="repdfreader", action='store_true', default=0, help='Recreate a pdf_dig pdfreader structure if cached')
  p.add_argument('--resentence',  dest="resentence",  action='store_true', default=0, help='Recreate a pdf_dig sentence structure if cached')

if args.action == 'getM':
  p.add_argument('--cognitions', dest="cognitions", type=str, help='Cognitions to dig')
  args = p.parse_known_args()[0]
  
  if str(args.cognitions) == 'None':
    session['cognitions'] = [x for x in listdir(get_runPath() + "/../cognitions/") if x not in dirIsTemplate]
  else:
    session['cognitions'] = args.cognitions.split()    
elif args.action == 'getH':
  print(args.action)
  
###

### TO DO

p.add_argument('--annselftest', dest="annselftest", type=int, default=0, help='Create annotation for reader self-test')
  #p.add_argument('--expdf', dest="exPDF", type=int, default=1, help='Export annotations to PDF')
  #p.add_argument('--exes', dest="exES", type=int, default=1, help='Export annotations to ES')    
###

### Call digger
args = p.parse_args()

diggerAction = importlib.import_module('lib.action_' + args.action) #.lower()
diggerAction.init(args,session)
###
