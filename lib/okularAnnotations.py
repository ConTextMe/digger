def AnnotationsFileInit(AnnotationsFileWriter, fileLoc):
  AnnotationsFileWriter.write('<?xml version="1.0" encoding="utf-8"?>\n')
  AnnotationsFileWriter.write('<!DOCTYPE documentInfo>\n')
  AnnotationsFileWriter.write('<documentInfo url="' + fileLoc + '">\n')
  AnnotationsFileWriter.write(' <pageList>\n')


def AnnotationPageBegin(AnnotationsFileWriter, page):
  AnnotationsFileWriter.write('  <page number="' + str(page-1) + '">\n')


def AnnotationPageEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('   </page>\n') 
  AnnotationsFileWriter.write('  </pageList>\n </documentInfo>')
 
 
def AnnotationListBegin(AnnotationsFileWriter, currDatetime, color='#0713ff', opacity='0.2'):
  AnnotationsFileWriter.write('   <annotationList>\n    <annotation type="4">\n     <base creationDate="' + currDatetime + '" flags="0" modifyDate="' + currDatetime + '"  opacity="' + opacity + '" author="digger" color="' + color + '" uniqueName="okular-{00000000-0000-0000-0000-000000000001}">\n      <boundary l="0" r="0" b="0" t="0"/>\n     </base>\n     <hl>\n')


def AnnotationQuad(AnnotationsFileWriter, size, coords):
  coords["posXBegin"] = round(coords["posXBegin"]/size["w"], 6) 
  coords["posXEnd"] = round(coords["posXEnd"]/size["w"], 6)
  coords["posYBegin"] = round(coords["posYBegin"]/size["h"], 6)
  coords["posYEnd"] = round(coords["posYEnd"]/size["h"], 6)
 
  AnnotationsFileWriter.write('      <quad ax="' + str(coords["posXBegin"]) + '" bx="' + str(coords["posXEnd"]) + '" dx="'+ str(coords["posXBegin"]) + '" cx="' + str(coords["posXEnd"]) + '" dy="' + str(coords["posYEnd"]) + '" cy="' + str(coords["posYEnd"])  + '" by="' + str(coords["posYBegin"]) + '" ay="' + str(coords["posYBegin"]) + '" feather="1"/>\n')

    
def AnnotationListEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('     </hl>\n      </annotation>\n    </annotationList>\n')
    
