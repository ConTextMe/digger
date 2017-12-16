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

def struct_annotate(args, session, sentenceStruct):
  import shutil
  from os.path import expanduser
    
  AnnotationsFileWriter = open(session['mainPath'] + session['docFilename'] + '.xml','w')
  AnnotationsBegin(AnnotationsFileWriter, args.fileLoc)
  for page in sentenceStruct:
    AnnotationPageBegin(AnnotationsFileWriter,int(page))
    AnnotationListBegin(AnnotationsFileWriter,session)
    for sentence in sentenceStruct[page]:
      if "p" in sentenceStruct[page][sentence]:
        for word in sentenceStruct[page][sentence]["p"]:
          AnnotationQuad(AnnotationsFileWriter,sentenceStruct[page]["size"],sentenceStruct[page][sentence]["p"][word])
    AnnotationListEnd(AnnotationsFileWriter)
    AnnotationPageEnd(AnnotationsFileWriter)
  AnnotationEnd(AnnotationsFileWriter)
  
  AnnotationsFileWriter.close()
  shutil.move(session['tmp_path'] + session['docFilename'] + '.xml', str(expanduser("~")) + '/.local/share/okular/docdata/' + session['docFilename'] + '.xml')  

def AnnotationsBegin(AnnotationsFileWriter, fileLoc):
  AnnotationsFileWriter.write('<?xml version="1.0" encoding="utf-8"?>\n')
  AnnotationsFileWriter.write('<!DOCTYPE documentInfo>\n')
  AnnotationsFileWriter.write('<documentInfo url="' + fileLoc + '">\n')
  AnnotationsFileWriter.write(' <pageList>\n')

def AnnotationEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('  </pageList>\n </documentInfo>') 

def AnnotationPageBegin(AnnotationsFileWriter, page):
  AnnotationsFileWriter.write('  <page number="' + str(page-1) + '">\n')

def AnnotationPageEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('   </page>\n') 
 
def AnnotationListBegin(AnnotationsFileWriter, session, color='#0713ff', opacity='0.2'):
  AnnotationsFileWriter.write('   <annotationList>\n    <annotation type="4">\n     <base creationDate="' + session['currDatetime'] + '" flags="0" modifyDate="' + session['currDatetime'] + '"  opacity="' + opacity + '" author="digger" color="' + color + '" uniqueName="okular-{00000000-0000-0000-0000-000000000001}">\n      <boundary l="0" r="0" b="0" t="0"/>\n     </base>\n     <hl>\n')

def AnnotationQuad(AnnotationsFileWriter, size, word):
  word["posXBegin"] = round(word["posXBegin"]/size["w"], 6) 
  word["posXEnd"] = round(word["posXEnd"]/size["w"], 6)
  word["posYBegin"] = round(word["posYBegin"]/size["h"], 6)
  word["posYEnd"] = round(word["posYEnd"]/size["h"], 6)

  AnnotationsFileWriter.write('      <quad ax="' + str(word["posXBegin"]) + '" bx="' + str(word["posXEnd"]) + '" dx="'+ str(word["posXBegin"]) + '" cx="' + str(word["posXEnd"]) + '" dy="' + str(word["posYEnd"]) + '" cy="' + str(word["posYEnd"])  + '" by="' + str(word["posYBegin"]) + '" ay="' + str(word["posYBegin"]) + '" feather="1"/>\n')


def AnnotationListEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('     </hl>\n      </annotation>\n    </annotationList>\n')
