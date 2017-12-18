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
def annotateAsDigestXML(args, session, sentenceStruct, annotationStruct):
  import shutil
  from os.path import expanduser
  
  digestFilename = str(session['size']) + '.' + session['contentHash'] + '.pdf'
  AnnotationsFileWriter = open(session['mainPath'] + digestFilename + '.xml','w')
  AnnotationsBegin(args, session, AnnotationsFileWriter)
  for page in annotationStruct:
    AnnotationPageBegin(AnnotationsFileWriter,int(page))
    for ex in annotationStruct[page]:    
      AnnotationOptsBegin(AnnotationsFileWriter,session, session['annotationSettings'][ex])      
      for sentence in annotationStruct[page][ex]:
        for wordNumber in annotationStruct[page][ex][sentence]:
          wordNumberFitted = "{:0>3.0f}".format(int(wordNumber))
          #print(sentenceStruct[page][sentence]['pos'])
          AnnotationQuad(AnnotationsFileWriter,sentenceStruct[page]["par"]["size"],sentenceStruct[page][sentence]['pos'][wordNumberFitted])
      AnnotationOptsEnd(AnnotationsFileWriter)
    AnnotationPageEnd(AnnotationsFileWriter)
  AnnotationEnd(AnnotationsFileWriter)
  
  AnnotationsFileWriter.close()
  shutil.move(session['mainPath'] + digestFilename + '.xml', str(expanduser("~")) + '/.local/share/okular/docdata/' + digestFilename + '.xml')  

def AnnotationsBegin(args, session, AnnotationsFileWriter):
  AnnotationsFileWriter.write('<?xml version="1.0" encoding="utf-8"?>\n')
  AnnotationsFileWriter.write('<!DOCTYPE documentInfo>\n')
  AnnotationsFileWriter.write('<documentInfo url="' + str(session['size']) + '.' + session['contentHash'] + '.pdf">\n')
  AnnotationsFileWriter.write(' <pageList>\n')

def AnnotationEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('  </pageList>\n </documentInfo>') 

def AnnotationPageBegin(AnnotationsFileWriter, page):
  AnnotationsFileWriter.write('  <page number="' + str(page-1) + '">\n   <annotationList>\n')

def AnnotationPageEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('    </annotationList>\n   </page>\n') 
 
def AnnotationOptsBegin(AnnotationsFileWriter, session, opts):
  AnnotationsFileWriter.write('    <annotation type="4">\n     <base creationDate="' + session['currDatetime'] + '" flags="0" modifyDate="' + session['currDatetime'] + '"  opacity="' + opts['opacity'] + '" author="digger" color="' + opts['color'] + '" uniqueName="okular-{00000000-0000-0000-0000-000000000001}">\n      <boundary l="0" r="0" b="0" t="0"/>\n     </base>\n     <hl>\n')

def AnnotationQuad(AnnotationsFileWriter, size, word):
  word["posXBegin"] = round(word["posXBegin"]/size["w"], 6) 
  word["posXEnd"] = round(word["posXEnd"]/size["w"], 6)
  word["posYBegin"] = round(word["posYBegin"]/size["h"], 6)
  word["posYEnd"] = round(word["posYEnd"]/size["h"], 6)

  AnnotationsFileWriter.write('      <quad ax="' + str(word["posXBegin"]) + '" bx="' + str(word["posXEnd"]) + '" dx="'+ str(word["posXBegin"]) + '" cx="' + str(word["posXEnd"]) + '" dy="' + str(word["posYEnd"]) + '" cy="' + str(word["posYEnd"])  + '" by="' + str(word["posYBegin"]) + '" ay="' + str(word["posYBegin"]) + '" feather="1"/>\n')


def AnnotationOptsEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('     </hl>\n      </annotation>\n')
