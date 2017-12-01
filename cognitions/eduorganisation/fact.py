name = 'eduorganisation'

def fileInit(context, filename):
  ExportIndexdata='{"index":{"_index":"' + context + '","_type":"' + name + '"}}'
  ExportFile = '/tmp/ner/' + filename + '__' + name + '.nlp'
  ExportFileWriter = open(ExportFile,'w')
  ExportFileWriter.write(ExportIndexdata + '\n')
  return ExportFileWriter
  
  
def elasticExporter(match, ExportFileWriter, isbn, page, lineNum):
    data = {
      "isbn" : isbn,      
      "page" : page,       
      "line_abs" : lineNum,       
      "class" : name,
      "orgname" : match.fact.name,
      "tmp" : match.fact.tmp,
      "tmp2" : match.fact.tmp2,
      }
    ExportFileWriter.write(str(data) + '\n')


def annotationSettings():
  extractors = {}; extractors['color'] = "#0713ff"; extractors['opacity'] = "0.2"
  return extractors
