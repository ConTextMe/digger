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
  
  pagesText = ""  
  for pages in document:
    prevBlock = ""
    page = pages.page_no
    AnnotationsFileWriter.write('<page number="' + str(page-1) + '">\n')   
    for flow in pages:
        for block in flow:
            #print(block.bbox.as_tuple())
            currBlock = block
            random_seed(41)
            prevYCoord = 0
            for line in block:
                currYCoord = line.bbox.y1
                print("PRE: LineNum" + str(lineNum) + ", Text: " + line.text)
                if (currYCoord - prevYCoord) < 5:
                  continue
                if line.text.isdigit() and prevBlock != "" and currBlock != prevBlock:
                  continue
                if line.text[-1:] == ".":
                  textAdd = line.text + " "
                else:
                  textAdd = line.text + " "
                
                print("POST: LineNum" + str(lineNum) + ", Text: " + textAdd)
                pagesText += textAdd
                lineNum = lineNum + 1
                prevYCoord = currYCoord
            prevBlock = currBlock
    print(pagesText)
    #for ex in cognitions:
      #matches = extractor[ex]['ExtractorHandler'](pagesText)
      #for match in matches:
        #start, stop = match.span
        #if args.debug:
          #print("Digg result (page " + str(page) + ", line " + str(lineNum) +") : " + str(match.fact))
        #fact[ex].elasticExporter(match, extractor[ex]['FileWriter'], isbn, page, lineNum)
        ##annotate(AnnotationsFileWriter, AnnotationMode, currDatetime, pages, line, start, stop, annotationSettings[ex]['color'], annotationSettings[ex]['opacity'])                    
                    
##
