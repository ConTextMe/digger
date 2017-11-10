
def init(context, docFilename, cognitions):
  import importlib
  extractor = {}
  
  for ex in cognitions:
    extractor[ex] = {}
    facts = importlib.import_module('cognitions.' + ex.lower() + '.fact')
    grammar = importlib.import_module('cognitions.' + ex.lower() + '.grammar')  
    extractor[ex]['FileWriter'] = facts.fileInit(context, docFilename)
    extractor[ex]['ExtractorHandler'] = eval('grammar.' + ex + 'Extractor')()
  return extractor


def ExportFileClose(extractor, cognitions):
  for ex in cognitions:
    extractor[ex]['FileWriter'].close() 
