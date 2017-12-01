#! /usr/bin/env python
# -*- coding: utf-8 -*-

## ## ## ## ## python 3 only ## ## ## ## ## 


def digUsingNer(args, filename, extractor, AnnotationMode, AnnotationsFileWriter, currDatetime, isbn, cognitions):
  import popplerqt5
  import PyQt5
  from lib.okularAnnotations import annotate  
  import importlib
  import re
  
  lineNum = 0  
  fact = {}; annotationSettings = {}
  for ex in cognitions:
    fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    annotationSettings[ex] = fact[ex].annotationSettings()
    
  document = popplerqt5.Poppler.Document.load(args.fileLoc)

  for page in range(document.numPages()):
    textOnPage = []
    pages = document.page(page)
    AnnotationsFileWriter.write('<page number="' + str(page-1) + '">\n')   
    #print(pages.text(1,2))
    for text in pages.textList():
      textOnPage += str(text.text())
      print(text.text())
      a = text.boundingBox()
    
    #print(textOnPage)
   
    #for a in textSent:
      #print(a)
      
    #for ex in cognitions:
      #matches = extractor[ex]['ExtractorHandler'](textOnPage)
      #for match in matches:
        #start, stop = match.span
        #if args.debug:
          #print("Digg result (page " + str(page) + ", line " + str(lineNum) +") : " + str(match.fact))
        #fact[ex].elasticExporter(match, extractor[ex]['FileWriter'], isbn, page, lineNum)
        #annotate(AnnotationsFileWriter, AnnotationMode, currDatetime, pages, line, start, stop, annotationSettings[ex]['color'], annotationSettings[ex]['opacity'])           
                    
###

    #total_pages = pdf.get_n_pages()
    #print "Total num:", total_pages
    #print "-" * 30

    #for page_num in range(total_pages):
        #page = pdf.get_page(page_num)
        #rect = get_page_rectangle(page.get_size())
        #print page.get_text(style=1, rect=rect)
        #print "-" * 30
        
        #http://lucasvr.gobolinux.org/etc/pdfGrep
