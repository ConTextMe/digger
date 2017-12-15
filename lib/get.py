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

from collections import OrderedDict
import hashlib 

def getPDF(args):
  
  struct = OrderedDict()
  import pdfparser.poppler as pdf
  from random import sample
  from random import seed as random_seed  
  import importlib
  import re  
  flowArr = ''
  document = pdf.Document(args.fileLoc.encode())
  totalPages = document.no_of_pages
  isbn = ''
  pattern = '^ISBN\s[\d].*'  
  reCompiled = re.compile(pattern)

  if args.gettype == 'hash':
    for pages in document:
      pageNum = pages.page_no
      for flow in pages:
        for block in flow:
          flowArr += str(block.bbox.as_tuple())
          if pageNum < 6 or totalPages - pageNum < 6:
            for line in block:
              result = reCompiled.findall(line.text)
              if not result == []:
                struct['isbn'] = str(result[0]).split()[1]
    flowHash = hashlib.sha1(flowArr.encode('utf-8')).hexdigest()
    struct['hash'] = flowHash
  
  return struct
    
def getPDFAnnotations(args, mode):
  import popplerqt5
  import PyQt5
  
  annDict = OrderedDict()
  doc = popplerqt5.Poppler.Document.load(args.fileLoc)
  for pageNum in range(doc.numPages()): 
    page = doc.page(pageNum)
    annotations = page.annotations()
    (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
    annotationCount = 1
    if len(annotations) > 0:
      for annotation in annotations:
        if (isinstance(annotation, popplerqt5.Poppler.HighlightAnnotation)): 
          annContent = str(annotation.contents()).split('::')
          vp = annContent[1]
          schema = annContent[3]
          content = annContent[5]
          cdate = str(annotation.creationDate().toMSecsSinceEpoch())
          author = str(annotation.author())
          uniqueName = str(annotation.uniqueName())
          quads = annotation.highlightQuads()
          coords = OrderedDict()
          i = 1
          for quad in quads:
            coords[i] = (quad.points[0].x() * pwidth,
                    quad.points[0].y() * pheight,
                    quad.points[2].x() * pwidth,
                    quad.points[2].y() * pheight)
            i += 1
        
          if mode == 'page':
            if pageNum not in annDict:
              annDict[pageNum] = OrderedDict()   
            if annotationCount not in annDict[pageNum]:
              annDict[pageNum][annotationCount] = OrderedDict()  
            
            annDict[pageNum][annotationCount]['vp'] = vp
            annDict[pageNum][annotationCount]['schema'] = schema
            annDict[pageNum][annotationCount]['content'] = content
            annDict[pageNum][annotationCount]['cdate'] = cdate
            annDict[pageNum][annotationCount]['author'] = author
            annDict[pageNum][annotationCount]['uname'] = uniqueName
            annDict[pageNum][annotationCount]['coords'] = coords 
            
          elif mode == 'schema':
            if schema not in annDict:
              annDict[schema] = OrderedDict()   
            if annotationCount not in annDict[schema]:
              annDict[schema][annotationCount] = OrderedDict()  
              
            annDict[schema][annotationCount]['vp'] = vp
            annDict[schema][annotationCount]['page'] = pageNum
            annDict[schema][annotationCount]['content'] = content
            annDict[schema][annotationCount]['cdate'] = cdate
            annDict[schema][annotationCount]['author'] = author
            annDict[schema][annotationCount]['uname'] = uniqueName
            annDict[schema][annotationCount]['coords'] = coords 
            
          elif mode == 'vp':
            if vp not in annDict:
              annDict[vp] = OrderedDict()   
            if annotationCount not in annDict[vp]:
              annDict[vp][annotationCount] = OrderedDict()  
              
            annDict[vp][annotationCount]['schema'] = schema
            annDict[vp][annotationCount]['page'] = pageNum
            annDict[vp][annotationCount]['content'] = content
            annDict[vp][annotationCount]['cdate'] = cdate
            annDict[vp][annotationCount]['author'] = author  
            annDict[vp][annotationCount]['uname'] = uniqueName
            annDict[vp][annotationCount]['coords'] = coords            
            
          elif mode == 'author':
            if author not in annDict:
              annDict[author] = OrderedDict()   
            if annotationCount not in annDict[author]:
              annDict[author][annotationCount] = OrderedDict()  
              
            annDict[author][annotationCount]['vp'] = vp            
            annDict[author][annotationCount]['schema'] = schema
            annDict[author][annotationCount]['page'] = pageNum
            annDict[author][annotationCount]['content'] = content
            annDict[author][annotationCount]['cdate'] = cdate
            annDict[author][annotationCount]['uname'] = uniqueName
            annDict[author][annotationCount]['coords'] = coords                        

          annotationCount += 1
    
  return annDict
