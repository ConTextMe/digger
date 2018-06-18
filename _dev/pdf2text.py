#! /usr/bin/env python

import pdfparser.poppler as pdf
import sys

d=pdf.Document(sys.argv[1])

print('<?xml version="1.0" encoding="utf-8"?>')
print('<!DOCTYPE documentInfo>')
print('<documentInfo url="/tmp/2/_tmp/11.pdf">')
print('<pageList>')
for p in d:
    print('<page number="' + str(p.page_no) + '">')
    print('   <annotationList>')
    print('    <annotation type="4">')
    print('     <base creationDate="2017-11-05T21:11:11" flags="0" modifyDate="2017-11-05T21:11:11" color="#ffff00" author="ConTextMeBot" uniqueName="okular-{f1e8fd00-8246-4b98-b9c8-0d6cc38fc28e}"></base>')
    print('<hl>')  
    for f in p:
        for b in f:
            for l in b:
              pos = -1
              for i in l.text.split():
                pos = pos
                boxCoordinates1 = l.char_bboxes[pos].as_tuple()
                x11 = round(boxCoordinates1[0]/p.size[0], 6) 
                y11 = round(boxCoordinates1[1]/p.size[1], 6)
                x12 = round(boxCoordinates1[2]/p.size[0], 6)
                y12 = round(boxCoordinates1[3]/p.size[1], 6)
                
                pos = pos + len(i)
                boxCoordinates2 = l.char_bboxes[pos].as_tuple()
                x21 = round(boxCoordinates2[0]/p.size[0], 6) 
                y21 = round(boxCoordinates2[1]/p.size[1], 6)
                x22 = round(boxCoordinates2[2]/p.size[0], 6)
                y22 = round(boxCoordinates2[3]/p.size[1], 6)
                
                coeff = 0.020000
                xml = '<quad dx="'+ str(x12+coeff) + '" dy="' + str(y22) + '" cx="' + str(x22+coeff) + '" cy="' + str(y22) + '" bx="' + str(x22+coeff) + '" by="' + str(y11) + '" ax="' + str(x12+coeff) + '" ay="' + str(y11) + '" feather="1"/>'
                #print(i)
                print(xml)
                
                #print(y11, y12, y21, y22)
                #print(x11, x12, x21, x22)
    print('</hl></annotation></annotationList></page>') 
print('</pageList></documentInfo>')
