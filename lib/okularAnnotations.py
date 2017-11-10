def AnnotationsFileInit(AnnotationsFileWriter, fileLoc):
  AnnotationsFileWriter.write('<?xml version="1.0" encoding="utf-8"?>\n')
  AnnotationsFileWriter.write('<!DOCTYPE documentInfo>\n')
  AnnotationsFileWriter.write('<documentInfo url="' + fileLoc + '">\n')
  AnnotationsFileWriter.write('<pageList>\n')

def AnnotationBegin(currDatetime,color,opacity):
  return '<annotationList>\n<annotation type="4">\n<base creationDate="' + currDatetime + '" flags="0" modifyDate="' + currDatetime + '"  opacity="' + opacity + '" author="contextme_ner" color="' + color + '" uniqueName="okular-{00000000-0000-0000-0000-000000000001}"><boundary l="0" r="0" b="0" t="0"/></base>\n<hl>\n'
  
  
def AnnotationEnd():
  return '</hl>\n</annotation>\n</annotationList>\n'


def annotate(AnnotationsFileWriter, AnnotationMode, currDatetime, pages, line, start, stop, color, opacity):
  stop = stop - 1
  boxCoordinates1 = line.char_bboxes[start].as_tuple()
  x11 = round(boxCoordinates1[0]/pages.size[0], 6) 
  y11 = round(boxCoordinates1[1]/pages.size[1], 6)
  boxCoordinates2 = line.char_bboxes[stop].as_tuple()
  x22 = round(boxCoordinates2[2]/pages.size[0], 6)
  y22 = round(boxCoordinates2[3]/pages.size[1], 6)
  if AnnotationMode == 'multiple':
    AnnotationsFileWriter.write(AnnotationBegin(currDatetime, color, opacity))
  AnnotationsFileWriter.write('')  
  quad = '<quad ax="' + str(x11) + '" bx="' + str(x22) + '" dx="'+ str(x11) + '" cx="' + str(x22) + '" dy="' + str(y22) + '" cy="' + str(y22)  + '" by="' + str(y11) + '" ay="' + str(y11) + '" feather="1"/>\n'
  AnnotationsFileWriter.write(quad)
  if AnnotationMode == 'multiple':
    AnnotationsFileWriter.write(AnnotationEnd())  
