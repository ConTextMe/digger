# -*- coding: utf-8 -*-

#### FINAL SED
#popen("sed -i 's/None/\"None\"/g' /tmp/ner/*.nlp")
#popen("sed -i 's/\\x27/\"/g' /tmp/ner/*.nlp")
####

def nerFromPDF(fileLoc, filename, extractor, AnnotationMode, AnnotationsFileWriter, currDatetime, isbn, context, cognitions):
  import pdfparser.poppler as pdf
  import popplerqt5
  import PyQt5
  from lib.okularAnnotations import annotate  
  from random import sample
  from random import seed as random_seed  
  import importlib
  lineNum = 0  
  fact = {}; annotationSettings = {}
  for ex in cognitions:
    fact[ex] = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    annotationSettings[ex] = fact[ex].annotationSettings()
    
    doc = popplerqt5.Poppler.Document.load(fileLoc)
    for i in range(doc.numPages()):
        print("========= PAGE {} =========".format(i+1))
        page = doc.page(i)
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        if len(annotations) > 0:
            for annotation in annotations:
                if  isinstance(annotation, popplerqt5.Poppler.Annotation):
                    if(isinstance(annotation, popplerqt5.Poppler.HighlightAnnotation)):
                        quads = annotation.highlightQuads()
                        txt = ""
                        for quad in quads:
                            rect = (quad.points[0].x() * pwidth,
                                    quad.points[0].y() * pheight,
                                    quad.points[2].x() * pwidth,
                                    quad.points[2].y() * pheight)
                            bdy = PyQt5.QtCore.QRectF()
                            bdy.setCoords(*rect)
                            txt = txt + str(page.text(bdy)) + ' '

                        #print("========= ANNOTATION =========")
                        #print(str(txt))
                        #print(str(dir(annotation)))                        
                        print(str(annotation.contents()))    
