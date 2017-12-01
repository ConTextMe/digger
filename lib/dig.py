#! /usr/bin/env python
# -*- coding: utf-8 -*-

## ## ## ## ## python 3 only ## ## ## ## ## 


def digUsingNer(args, filename, extractor, AnnotationMode, AnnotationsFileWriter, currDatetime, isbn, cognitions):
  import pdfparser.poppler as pdf
  from lib.okularAnnotations import annotate  
  from random import sample
  from random import seed as random_seed  
  import importlib
  lineNum = 0  
  fact = {}; annotationSettings = {}
  for ex in cognitions:
    fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    annotationSettings[ex] = fact[ex].annotationSettings()
    
  document = pdf.Document(args.fileLoc.encode())
  
  for pages in document:
    page = pages.page_no
    AnnotationsFileWriter.write('<page number="' + str(page-1) + '">\n')   
    for flow in pages:
        for block in flow:
            random_seed(41)
            for line in block:
                curLineText = line.text
                lineNum = lineNum + 1
                for ex in cognitions:
                  matches = extractor[ex]['ExtractorHandler'](curLineText)
                  for match in matches:
                    start, stop = match.span
                    if args.debug:
                      print("Digg result (page " + str(page) + ", line " + str(lineNum) +") : " + str(match.fact))
                    fact[ex].elasticExporter(match, extractor[ex]['FileWriter'], isbn, page, lineNum)
                    annotate(AnnotationsFileWriter, AnnotationMode, currDatetime, pages, line, start, stop, annotationSettings[ex]['color'], annotationSettings[ex]['opacity'])                    
                    
##
