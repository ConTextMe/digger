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
###

### VARS
context = sys.argv[1]
fileLoc = sys.argv[2]
cognitions = sys.argv[3].split()
currDatetime = datetime.datetime.now()
currDatetime = currDatetime.strftime("%Y-%m-%dT%H:%M:%S")
docFilename = str(os.path.getsize(fileLoc)) + '.' + os.path.basename(fileLoc)
ExtractorHandler = {}
AnnotationMode = 'multiple'
###

### CONSTS
isbn = 00000
###

### DIR INIT
popen('mkdir -p /tmp/ner')
popen('rm /tmp/ner/' + docFilename + '_*.nlp')
###

### Annotation init
from lib.okularAnnotations import AnnotationsFileInit, annotate
AnnotationsFileWriter = open('/tmp/ner/' + docFilename + '.xml','w')
AnnotationsFileInit(AnnotationsFileWriter, fileLoc)
###

### EXTRACTORS
from lib.extractors import init, ExportFileClose
extractor = init(context, docFilename, cognitions)
from lib.pdf2ner import nerFromPDF
nerFromPDF(fileLoc, docFilename, extractor, AnnotationMode, AnnotationsFileWriter, currDatetime, isbn, context, cognitions)
ExportFileClose(extractor, cognitions)
###

### CLOSE ANNOTATION & MV
AnnotationsFileWriter.close()
shutil.move('/tmp/ner/' + docFilename + '.xml', str(expanduser("~")) + '/.local/share/okular/docdata/' + docFilename + '.xml')
###

### FINAL SED
popen("sed -i 's/None/\"None\"/g' /tmp/ner/*.nlp")
popen("sed -i 's/\\x27/\"/g' /tmp/ner/*.nlp")
###
