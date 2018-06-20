#! /usr/bin/env python
# -*- coding: utf-8 -*-

## ## ## ## ## python 3 only ## ## ## ## ## 

### SYS
import sys
import shutil
import os
import re
from os import popen
from os.path import expanduser
import datetime
import pdfparser.poppler as pdf


fileLoc = sys.argv[1]
filename = str(os.path.getsize(fileLoc)) + '.' + os.path.basename(fileLoc)

def pdf2ner(filename):
  lineNum = 0
  singleAnnotationMode = 0
  
  document = pdf.Document(fileLoc.encode())
  
  for pages in document:
      pageNum = str(pages.page_no)
      #print('PAGE: ' + str(dir(pages)))
        
      for flow in pages:
          #print('FLOW: ' + str(dir(flow)))

          for block in flow:
              #print('BLOCK: ' + str(dir(block)))            
              for line in block:
                  #print('LINE: ' + str(dir(line)))                
                  curLineText = line.text
                  lineNum = lineNum + 1
                  #print('Current line (#' + str(lineNum) + '): ' + curLineText)
                  
                  #Names

###


pdf2ner(filename)


#PAGE: [', 'page_no', 'size']
#BLOCK: [', 'bbox']
#LINE: ['bbox', 'char_bboxes', 'char_fonts', 'text']
