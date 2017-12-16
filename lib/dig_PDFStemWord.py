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

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine
from collections import defaultdict, OrderedDict
import multiprocessing

def getPDFStruct(args,session):
  import time

  startTime = time.time()
  relPageTimePrev = startTime
  all_texts = 0
  word_margin = 10
  boxes_flow = 0
  line_margin = 0.3

  documentFile = open(session['srcPath'] + session['srcHash'] + '.pdf', 'rb')
  parser = PDFParser(documentFile)
  document = PDFDocument(parser, "")
  rsrcmgr = PDFResourceManager()
  laparams = LAParams()
  for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow", "output_type"):
    paramv = locals().get(param, None)
    if paramv is not None:
        setattr(laparams, param, paramv)  
  device = PDFPageWordStemmer(rsrcmgr, laparams=laparams)
  interpreter = PDFPageInterpreter(rsrcmgr, device)
  
  pageNum = 1
  struct = OrderedDict()
  que = multiprocessing.Queue()
  parent_conn, child_conn = multiprocessing.Pipe()
  
  for page in PDFPage.create_pages(document):
    beginTime = time.time()
    
    p = multiprocessing.Process(target=doPDFPageInterpret,args=(child_conn,interpreter, page, que, device, struct, pageNum))
    p.start()   
    p.join(timeout=2)
    if p.is_alive():
      struct[pageNum] = 0
      print("Skipped page " + str(pageNum))
      p.terminate()
      p.join()
     
    else: 
      struct[pageNum]=parent_conn.recv()
    
    endTime = time.time()
    p.terminate()
    #print('Page: ' + str(pageNum) + ' , AbsTime: ' + str(beginTime - startTime) +  ' , RelTime: ' + str(endTime - beginTime))
    pageNum += 1
  
  return struct

def doPDFPageInterpret(child_conn, interpreter, page, que, device, struct, pageNum):
  interpreter.process_page(page)
  child_conn.send(device.rows)
  child_conn.close()
  

class PDFPageWordStemmer(PDFPageAggregator):
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
          dChar = 0
          for child in item:
            if isinstance(child, (LTChar, LTAnno)):
              charText = child.get_text()
              charTextOrd = ord(charText)
              if isinstance(child, (LTChar)):
                charCoords[charsNumber]["x0"] = round(child.x0, 6)
                charCoords[charsNumber]["x1"] = round(child.x1, 6)
                charCoords[charsNumber]["y0"] = round(child.y0, 6)            
                charCoords[charsNumber]["y1"] = round(child.y1, 6)
                charCoords[charsNumber]["ord"] = charTextOrd
                charCoords[charsNumber]["char"] = charText                

              #print("1. Char: " + charText + " , Ord: " + str(charTextOrd) + " full: " + str(child))
              if charTextOrd in (10, 32, 33, 34, 40, 41, 44, 45, 46, 58, 59, 63, 173): #\n_\s_!_"_(_)_,_-_._:_;_?_\xad
                #if isinstance(child, (LTChar)) and charCoords[charsNumber]["y0"] == 540.131: print("word: '" + word + "', ord : " + str(charTextOrd) + ", chNum : " + str(charsNumber) + ", ch : " + str(child))
                wordLen = len(word)
                if wordLen == 0:
                  word = ''
                else:
                  dChar = 1
                charWordBeginWith = charsNumber-wordLen

                if isinstance(child,LTAnno) and charTextOrd == 10:
                  #wordLen = wordLen - 1
                  if wordLen >= 0:
                    charsNumber = charsNumber - 1
                    #print("3. word: " + word + " , Ord: " + str(charCoords[charsNumber]["ord"]) + " xCoord: " + str(charCoords[charsNumber]["x0"]) + " Len: " + str(wordLen))                                                          
                    if charCoords[charsNumber]["ord"] == 173:
                      charTextOrd = 00
                    elif charCoords[charsNumber]["ord"] == 46:  
                      word = word + '\\\\n'
                      charTextOrd = 00
                    elif charCoords[charsNumber]["ord"] == 32:  
                      charTextOrd = 32
                    else:
                      #print(str(child) + ' : ' + str(charCoords[charsNumber]["ord"])+ " : '" + chr(charCoords[charsNumber]["ord"]) + "', word: " + word)
                      word = word + ' '
                      charTextOrd = 32
                    # BUG end char not highlighed
                
                if wordLen > 0:
                  y0Fitted = "{:0>11.6f}".format(charCoords[charsNumber]["y0"])
                  x0Fitted = "{:0>11.6f}".format(charCoords[charWordBeginWith]["x0"])
                  #print(y0Fitted)
                  if y0Fitted not in self.rows["strings"]:
                    self.rows["strings"][y0Fitted] = OrderedDict()
                  #if charCoords[charsNumber]["x0"] not in self.rows["strings"][charCoords[charWordBeginWith]["y0"]]:
                    #self.rows["strings"][y0Fitted][x0Fitted] = OrderedDict()
                  
                  self.rows["strings"][y0Fitted][x0Fitted] = { "posXBegin": charCoords[charWordBeginWith]["x0"], "posXEnd" : charCoords[charsNumber]["x0"], "posYBegin" : self.rows["size"]["h"] - charCoords[charsNumber]["y0"] - 0.2, "posYEnd" : self.rows["size"]["h"] - charCoords[charsNumber]["y1"] + 2, "len" : wordLen, "word" : word, "charEndPos" : charsNumber, "dChar" : charTextOrd, "absLine" : self.stringNumberAbs }
                
                  #print(" p: " + str(pageNumber) + " s: " + str(y0Fitted) + " sAbs: " + str(self.stringNumberAbs) + " w: " + str(charCoords[charsNumber]["x0"]) + " text: " + word) 
                wordNumber = wordNumber +1
                word = ''
                
                if isinstance(child,LTAnno) and charTextOrd == 10: 
                  self.stringNumberAbs += 1
                  self.stringNumber += 1
              
              charCoordsprev = charCoords
              charsNumber = charsNumber +1
              if dChar == 1: 
                dChar = 0
              else: 
                word += charText
              
          word = ' '.join(word.split())
          for child in item:
            render(child, pageNumber,stringNumber, stringNumberAbs)
        return
      self.rows = OrderedDict()
      self.rows["size"] = {"h" : ltpage.height, "w" : ltpage.width }
      self.rows["strings"] = OrderedDict()
      render(ltpage, ltpage.pageid,self.stringNumber, self.stringNumberAbs)
      self.stringNumber = 1
      self.result = ltpage
      #print("Page : " + str(ltpage.pageid))
