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

#@profile
def preaction(args, session):
  from os import path, readlink
  if session['preAction'] == 'download':
    download(args, session)
  elif session['preAction'] == 'genPDF':
    genPDF(args, session)
  elif session['preAction'] == 'cp':
    cp(args, session)
  if path.islink(session['srcPath'] + session['srcHash'] + '.pdf'):
    session['contentHash'] = readlink(session['srcPath'] + session['srcHash'] + '.pdf').split('/')[-1].split('.')[0]
  else:
    session = PDFFastRead(args, session)
  
  session['size'] = path.getsize(session['srcPath'] + session['srcHash'] + '.pdf')
  return session
    
def download(args, session):
  import sys, os
  import urllib.request

  if session['srcType'] == 'url':
    if os.path.isfile(session['srcPath'] + session['srcHash'] + '.pdf'):
      print('Using cached')
    else:
      urllib.request.urlretrieve(args.src, session['srcPath'] + session['srcHash'] + '.pdf')
  else:
    sys.exit("non-url")  

def genPDF(args, session):
  import sys, os

  if session['srcType'] == 'url':
    if os.path.isfile(session['srcPath'] + session['srcHash'] + '.pdf'):
      print('Using cached')
    else:
      from weasyprint import HTML
      HTML(args.src).write_pdf(session['srcPath'] + session['srcHash'] + '.pdf')
  else:
    sys.exit("non-url")  
  
def cp(args, session):
  from shutil import copyfile
  copyfile(args.src, session['srcPath'] + session['srcHash'] + '.pdf')

#@profile    
def PDFFastRead(args, session):
  import pdfparser.poppler as pdf
  from shutil import move
  from os import symlink
  import re
  import hashlib
  flowArr = ''
  fileSrc = session['srcPath'] + session['srcHash'] + '.pdf'
  document = pdf.Document(fileSrc.encode())
  totalPages = document.no_of_pages
  isbn = ''
  pattern = '^ISBN\s[\d].*'  
  reCompiled = re.compile(pattern)

  for pages in document:
    pageNum = pages.page_no
    for flow in pages:
      for block in flow:
        flowArr += str(block.bbox.as_tuple())
        if pageNum < 6 or totalPages - pageNum < 6:
          for line in block:
            result = reCompiled.findall(line.text)
            if not result == []:
              isbn = str(result[0]).split()[1]
  contentHash = hashlib.sha1(flowArr.encode('utf-8')).hexdigest()
  fileDst = session['prepocessedPath'] + contentHash + '.pdf'    
  move(fileSrc, fileDst)
  symlink(fileDst, fileSrc)
  session['contentHash'] = contentHash
  session['isbn'] = isbn
  
  return session
