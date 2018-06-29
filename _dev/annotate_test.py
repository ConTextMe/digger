...
for i in line.text.split():
  boxCoordinates1 = line.char_bboxes[pos].as_tuple()
  x11 = round(boxCoordinates1[0]/p.size[0], 6) 
  y11 = round(boxCoordinates1[1]/p.size[1], 6)
  x12 = round(boxCoordinates1[2]/p.size[0], 6)
  y12 = round(boxCoordinates1[3]/p.size[1], 6)
  
  try:
    pos = pos + len(i) + 1
    boxCoordinates2 = line.char_bboxes[pos].as_tuple()
    
  except IndexError:
    pos = pos - 2
    boxCoordinates2 = line.char_bboxes[pos].as_tuple()
    
  x21 = round(boxCoordinates2[0]/p.size[0], 6) 
  y21 = round(boxCoordinates2[1]/p.size[1], 6)
  x22 = round(boxCoordinates2[2]/p.size[0], 6)
  y22 = round(boxCoordinates2[3]/p.size[1], 6)

  quad = '\
  <quad ax="' + str(x11) + '" bx="' + str(x22) + '" dx="'+ str(x11) + '" cx="' + str(x22) + '" dy="' + str(y22) + '" cy="' + str(y22)  + '" by="' + str(y11) + '" ay="' + str(y11) + '" feather="1"/>\n'
  #print(i)
  AnnotationsFileWriter.write(quad)
