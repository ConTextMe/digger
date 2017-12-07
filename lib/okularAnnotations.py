def AnnotationsBegin(AnnotationsFileWriter, fileLoc):
  AnnotationsFileWriter.write('<?xml version="1.0" encoding="utf-8"?>\n')
  AnnotationsFileWriter.write('<!DOCTYPE documentInfo>\n')
  AnnotationsFileWriter.write('<documentInfo url="' + fileLoc + '">\n')
  AnnotationsFileWriter.write(' <pageList>\n')

def AnnotationEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('  </pageList>\n </documentInfo>') 

def AnnotationPageBegin(AnnotationsFileWriter, page):
  AnnotationsFileWriter.write('  <page number="' + str(page-1) + '">\n')

def AnnotationPageEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('   </page>\n') 
 
def AnnotationListBegin(AnnotationsFileWriter, currDatetime, color='#0713ff', opacity='0.2'):
  AnnotationsFileWriter.write('   <annotationList>\n    <annotation type="4">\n     <base creationDate="' + currDatetime + '" flags="0" modifyDate="' + currDatetime + '"  opacity="' + opacity + '" author="digger" color="' + color + '" uniqueName="okular-{00000000-0000-0000-0000-000000000001}">\n      <boundary l="0" r="0" b="0" t="0"/>\n     </base>\n     <hl>\n')

def AnnotationQuad(AnnotationsFileWriter, size, word):
  word["posXBegin"] = round(word["posXBegin"]/size["w"], 6) 
  word["posXEnd"] = round(word["posXEnd"]/size["w"], 6)
  word["posYBegin"] = round(word["posYBegin"]/size["h"], 6)
  word["posYEnd"] = round(word["posYEnd"]/size["h"], 6)

  AnnotationsFileWriter.write('      <quad ax="' + str(word["posXBegin"]) + '" bx="' + str(word["posXEnd"]) + '" dx="'+ str(word["posXBegin"]) + '" cx="' + str(word["posXEnd"]) + '" dy="' + str(word["posYEnd"]) + '" cy="' + str(word["posYEnd"])  + '" by="' + str(word["posYBegin"]) + '" ay="' + str(word["posYBegin"]) + '" feather="1"/>\n')


def AnnotationListEnd(AnnotationsFileWriter):
  AnnotationsFileWriter.write('     </hl>\n      </annotation>\n    </annotationList>\n')
    
