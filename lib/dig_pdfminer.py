#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine
from collections import defaultdict, OrderedDict
#from indexed import OrderedDict
from operator import itemgetter

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
          charCoords = OrderedDict()
                 
          word = ''
          for child in item:
            if isinstance(child, (LTChar, LTAnno)):
              charText = child.get_text()
              charTextOrd = ord(charText)
              if isinstance(child, (LTChar)):
                charCoords[charsNumber] = OrderedDict()
                charCoords[charsNumber] = {"1" : 1}
                charCoords[charsNumber]["x0"] = child.x0
                charCoords[charsNumber]["x1"] = child.x1
                charCoords[charsNumber]["y0"] = child.y0                
                charCoords[charsNumber]["y1"] = child.y1
                charCoords[charsNumber]["ord"] = charTextOrd
                charCoords[charsNumber]["char"] = charText                
                #print(child)

              #print("1. Char: " + charText + " , Ord: " + str(charTextOrd) + " full: " + str(child))
              if charTextOrd in (10, 32, 33, 34, 40, 41, 44, 45, 46, 58, 59, 63, 173): #\n_\s_!_"_(_)_,_-_._:_;_?_\xad
                #print("ord : " + str(charTextOrd) + ", chNum : " + str(charsNumber) + ", ch : " + str(child))
                wordLen = len(word)

                if isinstance(child,LTAnno) and charTextOrd == 10:
                  wordLen = wordLen - 1
                  if wordLen >= 0:
                    charsNumber = charsNumber - 1
                    #print("3. word: " + word + " , Ord: " + str(charCoords[charsNumber]["ord"]) + " xCoord: " + str(charCoords[charsNumber]["x0"]) + " Len: " + str(wordLen))                                                          
                    if charCoords[charsNumber]["ord"] == 173:
                      word = word
                    if charCoords[charsNumber]["ord"] == 46:  
                      word = word + '\n'                      
                    else:
                      word = word + ''
                    # BUG end char not highlighed
                
                if wordLen >= 0:
                  if charCoords[charsNumber]["y0"] not in self.rows[pageNumber]["strings"]:
                    self.rows[pageNumber]["strings"][charCoords[charsNumber]["y0"]] = OrderedDict()
                  if charCoords[charsNumber]["x0"] not in self.rows[pageNumber]["strings"][charCoords[charsNumber-wordLen]["y0"]]:
                    self.rows[pageNumber]["strings"][charCoords[charsNumber]["y0"]][charCoords[charsNumber-wordLen]["x0"]] = OrderedDict()
                  
                  self.rows[pageNumber]["strings"][charCoords[charsNumber]["y0"]][charCoords[charsNumber-wordLen]["x0"]] = { 0 : { "posXBegin": float("{0:.6f}".format(charCoords[charsNumber-wordLen]["x0"])), "posXEnd" : float("{0:.6f}".format(charCoords[charsNumber]["x0"])), "posYBegin" : float("{0:.6f}".format(self.rows[ltpage.pageid]["size"]["h"] - charCoords[charsNumber]["y0"] - 0.2)), "posYEnd" : float("{0:.6f}".format(self.rows[ltpage.pageid]["size"]["h"] - charCoords[charsNumber]["y1"] + 2)), "len" : wordLen, "text" : word, "charEnd" : charsNumber,  "absLine" : self.stringNumberAbs }}
                
                  #print(" p: " + str(pageNumber) + " s: " + str(charCoords[charsNumber]["y0"]) + " sAbs: " + str(self.stringNumberAbs) + " w: " + str(charCoords[charsNumber]["x0"]) + " text: " + word) 
                wordNumber = wordNumber +1
                word = ''
                
                if isinstance(child,LTAnno) and charTextOrd == 10: 
                  self.stringNumberAbs += 1
                  self.stringNumber += 1
              
              charCoordsprev = charCoords
              charsNumber = charsNumber +1
              word += charText
              
          word = ' '.join(word.split())
          for child in item:
            render(child, pageNumber,stringNumber, stringNumberAbs)
        return
      self.rows = OrderedDict()
      self.rows[ltpage.pageid] = OrderedDict()
      self.rows[ltpage.pageid]["strings"] = OrderedDict()
      self.rows[ltpage.pageid]["size"] = {"h" : ltpage.height, "w" : ltpage.width }
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
    #struct[pageNum] = OrderedDict(sorted(layout[pageNum].items(), key=itemgetter(1), reverse=True))
    pageNum += 1
   
  result = sorted(struct , key=struct.get , reverse = True)
  debug_struct(struct)
  #struct_annotate(args,struct,currDatetime,docFilename)
    
def debug_struct(struct):
  textCatenated = ""
  for page in struct:
    #print("#### P #### : " + str(page))   
    stringOrdered = OrderedDict(sorted(struct[page]["strings"].items(), key=lambda t: t[0], reverse = True))
    for string in stringOrdered:
      #print("  #### S #### : " + str(string))
      wordOrdered = OrderedDict(sorted(struct[page]["strings"][string].items(), key=lambda t: t[0]))      
      for word in wordOrdered:
        print(dir(wordOrdered))
        if struct[page]["strings"][string][word][0]["text"] == '.' and str(struct[page]["strings"][string][word][0]["text"]).isalpha():
          print("Ex")
        print("    #### W #### : " + str(word) + ", text: " + str(struct[page]["strings"][string][word][0]["text"]))
        textCatenated  += struct[page]["strings"][string][word][0]["text"]
  print(textCatenated)

def struct_annotate(args, struct, currDatetime, docFilename):
  import lib.okularAnnotations
  import shutil
  from os.path import expanduser
  
  AnnotationsFileWriter = open('/tmp/ner/' + docFilename + '.xml','w')
  lib.okularAnnotations.AnnotationsBegin(AnnotationsFileWriter, args.fileLoc)
  for page in struct:
    lib.okularAnnotations.AnnotationPageBegin(AnnotationsFileWriter,page)
    lib.okularAnnotations.AnnotationListBegin(AnnotationsFileWriter,currDatetime)
    for string in struct[page]["strings"]:
      for word in struct[page]["strings"][string]:
        lib.okularAnnotations.AnnotationQuad(AnnotationsFileWriter,struct[page]["size"],struct[page]["strings"][string][word][0])
    lib.okularAnnotations.AnnotationListEnd(AnnotationsFileWriter)
    lib.okularAnnotations.AnnotationPageEnd(AnnotationsFileWriter)
  lib.okularAnnotations.AnnotationEnd(AnnotationsFileWriter)
  
  AnnotationsFileWriter.close()
  shutil.move('/tmp/ner/' + docFilename + '.xml', str(expanduser("~")) + '/.local/share/okular/docdata/' + docFilename + '.xml')  
          
        

    #extracted_text = extracted_text.replace('\\xad\\n', '').replace(' \\n', ' ').replace('.\\n', ' ').replace('-\\n', '').replace('\\n', ' ')
