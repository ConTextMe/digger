#!/usr/bin/env python3.4
import popplerqt5
import PyQt5
import sys


def merge(target, src):
    dom=PyQt5.QtXml.QDomDocument()
    for pg_index in range(min(target.numPages(),src.numPages())):
        p_doc = target.page(pg_index)
        p_src = src.page(pg_index)
        for a in p_src.annotations():
            if not has_annotation(p_doc,a):
                a_el = dom.createElement("annotation")
                popplerqt5.Poppler.AnnotationUtils.storeAnnotation(a,a_el,dom)
                a_doc = popplerqt5.Poppler.AnnotationUtils.createAnnotation(a_el)
                p_doc.addAnnotation(a_doc)

def has_annotation(page,a):
    for pa in page.annotations():
        if pa.uniqueName() == a.uniqueName():
            return True
    return False
            
def save_pdf(pdf_doc,filename):
    c = pdf_doc.pdfConverter()
    c.setOutputFileName(filename)
    c.setPDFOptions(c.WithChanges)
    c.convert()
    
def load_pdf(filename):
    return popplerqt5.Poppler.Document.load(filename)


if __name__ == "__main__":
    doc = popplerqt5.Poppler.Document.load(sys.argv[1])
    total_annotations = 0
    for i in range(doc.numPages()):
        #print("========= PAGE {} =========".format(i+1))
        page = doc.page(i)
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        if len(annotations) > 0:
            for annotation in annotations:
                if  isinstance(annotation, popplerqt5.Poppler.Annotation):
                    total_annotations += 1
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
    
    
#['ACaret', 'AFileAttachment', 'AGeom', 'AHighlight', 'AInk', 'ALine', 'ALink', 'AMovie', 'AScreen', 'ASound', 'AStamp', 'AText', 'AWidget', 'A_BASE', 'Accepted', 'AdditionalActionType', 'Beveled', 'Cancelled', 'Cloudy', 'Completed', 'CursorEnteringAction', 'CursorLeavingAction', 'Dashed', 'Delete', 'DenyDelete', 'DenyPrint', 'DenyWrite', 'External', 'FixedRotation', 'FixedSize', 'Flag', 'FocusInAction', 'FocusOutAction', 'Group', 'Hidden', 'Highlight', 'HighlightType', 'Inset', 'LineEffect', 'LineStyle', 'Marked', 'MousePressedAction', 'MouseReleasedAction', 'NoEffect', 'None', 'PageClosingAction', 'PageInvisibleAction', 'PageOpeningAction', 'PageVisibleAction', 'Popup', 'Quad', 'Rejected', 'Reply', 'RevScope', 'RevType', 'Root', 'Solid', 'Squiggly', 'StrikeOut', 'Style', 'SubType', 'ToggleHidingOnMouse', 'Underline', 'Unmarked', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'author', 'boundary', 'contents', 'creationDate', 'flags', 'highlightQuads', 'highlightType', 'modificationDate', 'popup', 'revisionScope', 'revisionType', 'revisions', 'setAuthor', 'setBoundary', 'setContents', 'setCreationDate', 'setFlags', 'setHighlightQuads', 'setHighlightType', 'setModificationDate', 'setPopup', 'setStyle', 'setUniqueName', 'style', 'subType', 'uniqueName']


            
        
        
    
