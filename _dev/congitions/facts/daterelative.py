name = 'daterelaive'

def fileInit(context, filename):
  ExportIndexdata='{"index":{"_index":"' + context + '","_type":"' + name + '"}}'
  ExportFile = '/tmp/ner/' + filename + '__' + name + '.nlp'
  ExportFileWriter = open(ExportFile,'w')
  ExportFileWriter.write(ExportIndexdata + '\n')
  return ExportFileWriter
  
  
def elasticExporter(match, ExportFileWriter, isbn, pages, lineNum):
    data = {
      "isbn" : isbn,      
      "page" : pages.page_no,       
      "line_abs" : lineNum,       
      "class" : name,
      "yearrel" : match.fact.yearrel,
   
    }
    ExportFileWriter.write(str(data) + '\n')
