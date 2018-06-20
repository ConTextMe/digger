# -*- coding: utf-8 -*-
########    #######    ########    #######    ########    ########
##     / / / /    License    \ \ \ \ 
##    Copyleft culture, Copyright (C) is prohibited here
##    This work is licensed under a CC BY-SA 4.0
##    Creative Commons Attribution-ShareAlike 4.0 License
##    Refer to the http://creativecommons.org/licenses/by-sa/4.0/
########    #######    ########    #######    ########    ########
##    / / / /    Code Climate    \ \ \ \ 
##    Language = python3
##    Indent = space;    2 chars;
########    #######    ########    #######    ########    ########


def extractAnnSchema(sentenceStruct, AnnSchemaFileWriter):
  import re
  from functools import reduce
  tool = ''
  i = 1
  pattern = '.*@*::.*'
  reCompiled = re.compile(pattern)
  
  for page in sentenceStruct:
    for sentence in sentenceStruct[page]:  
      if "p" in sentenceStruct[page][sentence]:
        words = sentenceStruct[page][sentence]["s"].split()
        for word in words:
          result = reCompiled.findall(word)
          if not result == []:
            kv = result[0].split("::")
            value = kv[0].split("@")
            if "schema" in kv[1]:
              schema = 'Schema=' + value[1]
            elif "desc_ru" in kv[1]:
              schemaDescRu = 'SchemaDescRu=' + value[1]
            elif "item" in kv[1]:
              tool = tool + '<tool type="highlight" id="' + str(i) + '" name="' + str(value[1]) + '"><engine type="TextSelector" color="#' + str(value[3]) + '"><annotation viewpoint="' + str(value[2]) + '" opacity="0.3" type="Highlight" color="#' + str(value[3]) + '"/></engine><shortcut>' + str(i) + '</shortcut></tool>,'
              i += 1
  AnnSchemaFileWriter.write('[Reviews]\n')  
  AnnSchemaFileWriter.write('AnnotationTools=' + tool + '\n')
  AnnSchemaFileWriter.write(schema + '\n')
  AnnSchemaFileWriter.write(schemaDescRu + '\n\n')
  
  AnnSchemaFileWriter.write('[PageView]\n')
  AnnSchemaFileWriter.write('EditToolBarPlacement=1\n')
    
