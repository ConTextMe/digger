#! /usr/bin/env python
# -*- coding: utf-8 -*-

## ## ## ## ## python 3 only ## ## ## ## ## 


def nerFromPDF(fileLoc, filename, extractor, AnnotationMode, AnnotationsFileWriter, currDatetime, isbn, context, cognitions):
  import pdfparser.poppler as pdf
  from lib.okularAnnotations import annotate  
  from random import sample
  from random import seed as random_seed  
  import importlib
  lineNum = 0  
  fact = {}
  for ex in cognitions:
    fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')  
    
  document = pdf.Document(fileLoc.encode())
  
  for pages in document:
      AnnotationsFileWriter.write('<page number="' + str(pages.page_no-1) + '">\n')
      if AnnotationMode == 'single':
        color = '#98ff11'
        opacity = '0.3'
        AnnotationsFileWriter.write(AnnotationBegin(color,opacity))      
        
      for flow in pages:
          for block in flow:
              random_seed(41)
              for line in block:
                  curLineText = line.text
                  lineNum = lineNum + 1
                  #print('Current line (#' + str(lineNum) + '): ' + curLineText)          
                  for ex in cognitions:
                    matches = extractor[ex]['ExtractorHandler'](curLineText)
                    for match in matches:
                      start, stop = match.span
                      fact[ex].elasticExporter(match, extractor[ex]['FileWriter'], isbn, pages, lineNum)
                      annotate(AnnotationsFileWriter, AnnotationMode, currDatetime, pages, line, start, stop, )                    
                    

      if AnnotationMode == 'single':
        AnnotationsFileWriter.write(AnnotationEnd())
      AnnotationsFileWriter.write('</page>\n') 
  AnnotationsFileWriter.write('</pageList>\n</documentInfo>')
###
