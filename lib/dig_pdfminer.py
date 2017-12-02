#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine
from collections import defaultdict


class PDFPageDetailedAggregator(PDFPageAggregator):
    def __init__(self, rsrcmgr, pageno=1, laparams=None):
      PDFPageAggregator.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
      
      self.stringNumber = 1
      self.stringNumberAbs = 1
      
    def receive_layout(self, ltpage):     
      def render(item, pageNumber,stringNumber, stringNumberAbs):
          
        if isinstance(item, LTPage) or isinstance(item, LTTextBox):
          for child in item:
            render(child, pageNumber,stringNumber, stringNumberAbs)
        elif isinstance(item, LTTextLine):

          wordNumber = 1
          charsNumber = 1
          charCoords = defaultdict(lambda :defaultdict())
                 
          word = ''
          for child in item:
            if isinstance(child, (LTChar, LTAnno)):
              charText = child.get_text()
              charTextOrd = ord(charText)
              if isinstance(child, (LTChar)):
                charCoords[charsNumber]["x0"] = child.x0
                charCoords[charsNumber]["x1"] = child.x1
                charCoords[charsNumber]["y"] = child.y1
              #print(child)

              #print("Char: " + charText + " , Ord: " + str(charTextOrd))
              if charTextOrd in (32, 33, 44, 45, 173, 58, 59, 10):                
                if charTextOrd == 10:
                  self.stringNumberAbs += 1
                  self.stringNumber += 1
                  word = word + '\n'
                  wordLen = 0
                else:
                  wordLen = len(word)
                  
                if isinstance(child, (LTChar)):
                  #print("a : " + charCoords + ", ch : " + charsNumber)
                  wordXBegin = charCoords[charsNumber-wordLen+1]["x0"];
                  wordXEnd = charCoords[charsNumber]["x0"];
                  wordY = charCoords[charsNumber]["y"];
                else:
                  wordXBegin = 0; wordXEnd = 0; wordY = 0;    
                
                self.rows[pageNumber][self.stringNumber][wordNumber]["len"] = wordLen
                self.rows[pageNumber][self.stringNumber][wordNumber]["text"] = word
                self.rows[pageNumber][self.stringNumber][wordNumber]["posXBegin"] = wordXBegin
                self.rows[pageNumber][self.stringNumber][wordNumber]["posXEnd"] = wordXEnd
                self.rows[pageNumber][self.stringNumber][wordNumber]["posY"] = wordY
                self.rows[pageNumber][self.stringNumber][wordNumber]["charEnd"] = charsNumber
                self.rows[pageNumber][self.stringNumber][wordNumber]["absLine"] = self.stringNumberAbs                
                #print(" p: " + str(pageNumber) + " s: " + str(self.stringNumber) + " sAbs: " + str(self.stringNumberAbs) + " w: " + str(wordNumber))
                wordNumber = wordNumber +1
                word = ''
              
              charsNumber = charsNumber +1
              word += charText
              
          word = ' '.join(word.split())
          for child in item:
            render(child, pageNumber,stringNumber, stringNumberAbs)
        return
      self.rows = defaultdict(lambda :defaultdict(lambda :defaultdict(lambda :defaultdict())))
      render(ltpage, ltpage.pageid,self.stringNumber, self.stringNumberAbs)
      self.stringNumber = 1
      self.result = ltpage
      #print("Page : " + str(ltpage.pageid))
      
    

def digTextFromPDF(args, textFileWriter):
  import io, sys, re, timeit
  import time

  start_time = time.time()
  all_texts = 0
  word_margin = 10
  boxes_flow = 0
  line_margin = 0.3

  documentFile = open(args.fileLoc, 'rb')
  parser = PDFParser(documentFile)
  document = PDFDocument(parser, "")
  rsrcmgr = PDFResourceManager()
  laparams = LAParams()
  for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow", "output_type"):
    paramv = locals().get(param, None)
    if paramv is not None:
        setattr(laparams, param, paramv)  
  device = PDFPageDetailedAggregator(rsrcmgr, laparams=laparams)
  interpreter = PDFPageInterpreter(rsrcmgr, device)
  
  pageNum = 1
  textCatenated = ""
  for page in PDFPage.create_pages(document):
    pageTime = time.time()   
    interpreter.process_page(page)    
    layout = device.rows
    #print("#### P #### : " + str(pageNum))    
    for strings in layout[pageNum]:
      #print("#### S #### : " + str(strings))
      for words in layout[pageNum][strings]:
        #print("#### W #### : " + str(layout[pageNum][strings][words]["text"]))        
        textCatenated  += layout[pageNum][strings][words]["text"]
    print("--- %s seconds on page %s---" % (time.time() - pageTime, pageNum))
    pageNum += 1
    #extracted_text = getTextPerPage(layout)
  print(textCatenated)

def get_text_per_page(layout):
  import pdfminer.layout  
  import re
  extracted_text = ""
  for lt_obj in layout:
    if isinstance(lt_obj, pdfminer.layout.LTTextBox) or isinstance(lt_obj, pdfminer.layout.LTTextLine):
      for w_obj in lt_obj:
          #for a_obj in w_obj:
        extracted_text = re.split('.[0-9][0-9][0-9] \'|.[0-9][0-9][0-9] \"',str(w_obj))[1][:-2]
    extracted_text = extracted_text.replace('\\xad\\n', '').replace(' \\n', ' ').replace('.\\n', ' ').replace('-\\n', '').replace('\\n', ' ')
  return extracted_text
