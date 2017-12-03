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
                charCoords[charsNumber]["y0"] = child.y0                
                charCoords[charsNumber]["y1"] = child.y1
                #print(child)

              #print("Char: " + charText + " , Ord: " + str(charTextOrd))
              if charTextOrd in (10, 32, 33, 45, 46, 58, 59, 173): #\n_\s_,_._:_;_\xad
                #print("ord : " + str(charTextOrd) + ", chNum : " + str(charsNumber) + ", ch : " + str(child))
                if isinstance(child,LTAnno) and charTextOrd == 10: 
                  self.stringNumberAbs += 1
                  self.stringNumber += 1
                  word = word + '\\n'
                  wordLen = 0
                elif charTextOrd == 173: 
                  word = word + '\\xad'
                  wordLen = len(word)
                else:
                  wordLen = len(word)
                  
                if isinstance(child, (LTChar)):
                  wordXBegin = charCoords[charsNumber-wordLen]["x0"];
                  wordXEnd = charCoords[charsNumber]["x0"];
                  wordYBegin = charCoords[charsNumber]["y0"];
                  wordYEnd = charCoords[charsNumber]["y1"];                  
                else:
                  wordXBegin = 0; wordXEnd = 0; wordYBegin = 0; wordYEnd = 0;
                
                #print(" p: " + str(pageNumber) + " s: " + str(self.stringNumber) + " sAbs: " + str(self.stringNumberAbs) + " w: " + str(wordNumber))                
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["len"] = wordLen
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["text"] = word
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["posXBegin"] = float("{0:.6f}".format(wordXBegin))
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["posXEnd"] = float("{0:.6f}".format(wordXEnd))
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["posYBegin"] = float("{0:.6f}".format(wordYBegin))
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["posYEnd"] = float("{0:.6f}".format(wordYEnd))
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["charEnd"] = charsNumber
                self.rows[pageNumber]["strings"][self.stringNumber][wordNumber]["absLine"] = self.stringNumberAbs                
                wordNumber = wordNumber +1
                word = ''
              
              charsNumber = charsNumber +1
              word += charText
              
          word = ' '.join(word.split())
          for child in item:
            render(child, pageNumber,stringNumber, stringNumberAbs)
        return
      self.rows = defaultdict(lambda :defaultdict(lambda :defaultdict(lambda :defaultdict(lambda :defaultdict()))))
      self.rows[ltpage.pageid]["size"]["h"] = ltpage.height
      self.rows[ltpage.pageid]["size"]["w"] = ltpage.width
      render(ltpage, ltpage.pageid,self.stringNumber, self.stringNumberAbs)
      self.stringNumber = 1
      self.result = ltpage
      #print("Page : " + str(ltpage.pageid))
      
    

def digTextFromPDF(args, textFileWriter,currDatetime,docFilename):
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
  struct = defaultdict(lambda :defaultdict(lambda :defaultdict()))
  for page in PDFPage.create_pages(document):
    pageTime = time.time()   
    interpreter.process_page(page)    
    layout = device.rows
    struct[pageNum]=layout[pageNum]
    pageNum += 1
    
  #debug_struct(struct)
  struct_annotate(args,struct,currDatetime,docFilename)
    
def debug_struct(struct):
  textCatenated = ""
  for page in struct:
    print("#### P #### : " + str(page))    
    for string in struct[page]["strings"]:
      print("#### S #### : " + str(string))
      for word in struct[page]["strings"][string]:
        print("#### W #### : " + str(struct[page]["strings"][string][word]["text"]))        
        textCatenated  += struct[page]["strings"][string][word]["text"]

def struct_annotate(args, struct, currDatetime, docFilename):
  import lib.okularAnnotations
  import shutil
  from os.path import expanduser
  
  AnnotationsFileWriter = open('/tmp/ner/' + docFilename + '.xml','w')
  lib.okularAnnotations.AnnotationsFileInit(AnnotationsFileWriter, args.fileLoc)
  for page in struct:
    lib.okularAnnotations.AnnotationPageBegin(AnnotationsFileWriter,page)
    lib.okularAnnotations.AnnotationListBegin(AnnotationsFileWriter,currDatetime)
    for string in struct[page]["strings"]:
      for word in struct[page]["strings"][string]:
        lib.okularAnnotations.AnnotationQuad(AnnotationsFileWriter,struct[page]["size"],struct[page]["strings"][string][word])
    lib.okularAnnotations.AnnotationListEnd(AnnotationsFileWriter)
    lib.okularAnnotations.AnnotationPageEnd(AnnotationsFileWriter)
  
  AnnotationsFileWriter.close()
  shutil.move('/tmp/ner/' + docFilename + '.xml', str(expanduser("~")) + '/.local/share/okular/docdata/' + docFilename + '.xml')  
          
        

    #extracted_text = extracted_text.replace('\\xad\\n', '').replace(' \\n', ' ').replace('.\\n', ' ').replace('-\\n', '').replace('\\n', ' ')
