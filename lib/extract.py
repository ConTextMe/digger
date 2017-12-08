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


def nerFromPDF(fileLoc, filename, extractor, AnnotationMode, AnnotationsFileWriter, currDatetime, isbn, context, cognitions):
  import pdfparser.poppler as pdf
  import popplerqt5
  import PyQt5
  from lib.okularAnnotations import annotate  
  from random import sample
  from random import seed as random_seed  
  import importlib
  lineNum = 0  
  fact = {}; annotationSettings = {}
  for ex in cognitions:
    fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    annotationSettings[ex] = fact[ex].annotationSettings()
    
    doc = popplerqt5.Poppler.Document.load(fileLoc)
    for i in range(doc.numPages()):
        print("========= PAGE {} =========".format(i+1))
        page = doc.page(i)
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        if len(annotations) > 0:
            for annotation in annotations:
                if  isinstance(annotation, popplerqt5.Poppler.Annotation):
                    if(isinstance(annotation, popplerqt5.Poppler.HighlightAnnotation)):
                        quads = annotation.highlightQuads()
                        txt = ""
                        for quad in quads:
                            rect = (quad.points[0].x() * pwidth,
                                    quad.points[0].y() * pheight,
                                    quad.points[2].x() * pwidth,
                                    quad.points[2].y() * pheight)
                            bdy = PyQt5.QtCore.QRectF()
                            bdy.setCoords(*rect)
                            txt = txt + str(page.text(bdy)) + ' '

                        #print("========= ANNOTATION =========")
                        #print(str(txt))
                        #print(str(dir(annotation)))                        
                        print(str(annotation.contents()))    
    
  #document = pdf.Document(fileLoc.encode())
  
  #for pages in document:
      #AnnotationsFileWriter.write('<page number="' + str(pages.page_no-1) + '">\n')   
      #for flow in pages:
          #for block in flow:
              #random_seed(41)
              #for line in block:
                  #curLineText = line.text
                  #lineNum = lineNum + 1
                  ##print('Current line (#' + str(lineNum) + '): ' + curLineText)          
                  #for ex in cognitions:
                    #matches = extractor[ex]['ExtractorHandler'](curLineText)
                    #for match in matches:
                      #start, stop = match.span
                      #fact[ex].elasticExporter(match, extractor[ex]['FileWriter'], isbn, pages, lineNum)
                      #annotate(AnnotationsFileWriter, AnnotationMode, currDatetime, pages, line, start, stop, annotationSettings[ex]['color'], annotationSettings[ex]['opacity'])                    
                    
###
