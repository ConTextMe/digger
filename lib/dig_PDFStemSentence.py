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

def makeIntermStruct(struct):
  intermStruct = OrderedDict()
  for page in struct:
    if struct[page] == 0: continue
    if page not in intermStruct:
      intermStruct[page] = OrderedDict()
      intermStruct[page]["size"] = struct[page]["size"]
    if "strings" not in intermStruct[page]:
      intermStruct[page]["strings"] = OrderedDict()      
    stringOrdered = OrderedDict(sorted(struct[page]["strings"].items(), key=lambda t: t[0], reverse = True))
    stringNumber = 1
    for string in stringOrdered:
      stringNumberFitted = "{:0>2.0f}".format(stringNumber)
      if stringNumber not in intermStruct[page]["strings"]:
        intermStruct[page]["strings"][stringNumberFitted] = OrderedDict()
      wordOrdered = OrderedDict(sorted(struct[page]["strings"][string].items(), key=lambda t: t[0])) 
      wordNumber = 1
      for word in wordOrdered:
        wordNumberFitted = "{:0>2.0f}".format(wordNumber)
        intermStruct[page]["strings"][stringNumberFitted][wordNumberFitted] = struct[page]["strings"][string][word]
        wordNumber += 1
      stringNumber += 1
  return intermStruct
    
def makeSentenceStruct(struct):
  sentence = ''
  sentenceWords = OrderedDict()
  sentenceWordsMap = OrderedDict()
  wordNumber = 1
  sentenceRule = ''
  sentenceStemmer = 0
  
  sentenceStruct = OrderedDict()
  for page in struct:
    #print("#### P #### : " + str(page))   
    if page not in sentenceStruct:
      sentenceStruct[page] = OrderedDict()
      sentenceStruct[page]["par"] = {'size' : struct[page]["size"] }
    sentenceNumber = 1
    for string in struct[page]["strings"]:
      if sentenceNumber not in sentenceStruct[page]:
        sentenceStruct[page][sentenceNumber] = OrderedDict()
      #print("  #### S #### : " + str(string))
      for word in struct[page]["strings"][string]:
        wordStruct = struct[page]["strings"][string][word]["word"]
        dCharStruct = struct[page]["strings"][string][word]["dChar"]
        charEndPosStruct = struct[page]["strings"][string][word]["charEndPos"]
        wordPos = {"posXBegin" : struct[page]["strings"][string][word]["posXBegin"], "posXEnd" : struct[page]["strings"][string][word]["posXEnd"], "posYBegin" : struct[page]["strings"][string][word]["posYBegin"], "posYEnd" : struct[page]["strings"][string][word]["posYEnd"], "wordStruct" : wordStruct}
        
        sentencePart = wordStruct + chr(dCharStruct)
        #print("    #### W #### : " + word + ", word: '" + sentencePart + "'")
        #print("Page: " + str(page) + "', wordStruct : '" + str(wordStruct) + "', dCharStruct : '" + str(dCharStruct) + "', sentencePart: '" + str(sentencePart) + "'")

        if str(wordStruct) == '.\\\\n':
          sentence += '.'
          sentenceRule = 'directNewLine'          
        elif  dCharStruct == 46:
          
          if str("{:0>2.0f}".format(int(word)+1)) not in struct[page]["strings"][string]:
            sentenceRule = 'lastWordInString'
          else:
            if str("{:0>2.0f}".format(int(word)-1)) in struct[page]["strings"][string]:
              wordStructPrev  = struct[page]["strings"][string][str("{:0>2.0f}".format(int(word)-1))]["word"]
              dCharStructPrev = struct[page]["strings"][string][str("{:0>2.0f}".format(int(word)-1))]["dChar"]
            else:
              wordStructPrev  = ''
              dCharStructPrev = 00
            sentencePartPrev  = wordStructPrev + chr(dCharStructPrev)
            
            wordStructNext   = struct[page]["strings"][string][str("{:0>2.0f}".format(int(word)+1))]["word"]
            dCharStructNext  = struct[page]["strings"][string][str("{:0>2.0f}".format(int(word)+1))]["dChar"]
            sentencePartNext = wordStructNext + chr(dCharStructNext)
              
            if wordStruct.islower() and sentencePartNext == '..':
              sentenceRule = 'lowerPlusEllipsis'
              
            elif wordStruct.islower() and wordStructNext == ' ':
              sentenceRule = 'lowerPlusNextWordIsSpace'
            
            elif wordStruct.islower() and wordStructNext[0] == ' ' and wordStructNext[1].isupper():
              sentenceRule = 'lowerPlusNextCharIsSpace'
              
            
        elif str("{:0>2.0f}".format(int(string)+1)) not in struct[page]["strings"] and str("{:0>2.0f}".format(int(word)+1)) not in struct[page]["strings"][string]:
          sentenceRule = 'lastWordOnPage'
        
        sentence += sentencePart
        wordNumberFitted = "{:0>3.0f}".format(wordNumber)
        #print('wordNumber: ' + str(wordNumber) + ', sentencePart: ' + sentencePart)
        sentenceWords[wordNumberFitted] = wordPos
        sentenceWordsMap[wordNumberFitted] = len(sentence)
        if not sentenceRule == '':
          #print(str(page) + ", " + str(sentenceNumber) + ", " + sentence)
          sentenceStruct[page][sentenceNumber] = OrderedDict()
          sentenceStruct[page][sentenceNumber] = { 'sen' : sentence, 'pos' : sentenceWords, 'map' : sentenceWordsMap }
          
          #print("## Rule: '" + sentenceRule + "', sentence: " + sentence)
          sentenceNumber += 1
          sentence = ''
          sentenceWords = OrderedDict()
          sentenceWordsMap = OrderedDict()
          wordNumber = 1
          sentenceRule = ''
        else:
          wordNumber += 1
          
  return sentenceStruct

  
