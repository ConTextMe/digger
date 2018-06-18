import PyPDF2

inpf = '/home/e.istomin/Downloads/pdf_layer_new(1).pdf'
#inpf = '/media/storage/Library/Org/ConTextMe/products/_testpdfs/university_4.pdf'
infile = open(inpf, 'rb')
layfile = open('/media/storage/Library/Org/ConTextMe/products/_testpdfs/university_4.pdf', 'rb')
outfile = open('/tmp/1.pdf', 'wb')
inp = PyPDF2.PdfFileReader(infile)
o = PyPDF2.PdfFileWriter()
print(inp.trailer['/Root'])
###

#op = PyPDF2.pdf.PageObject.createBlankPage(
  #width=template_page_size.getWidth(),
  #height=template_page_size.getHeight()) 

###
o.write(outfile)
outfile.close()
infile.close()
##

outfile = open('/tmp/1.pdf', 'rb')
o = PyPDF2.PdfFileReader(outfile)
print('\n' + str(o.trailer['/Root']))

#print(dir(PyPDF2.pdf.PageObject))

#contentkey = PyPDF2.generic.NameObject('/Contents')
#resourcekey = PyPDF2.generic.NameObject('/Resources')
#propertieskey = PyPDF2.generic.NameObject('/Properties')
#properties = PyPDF2.generic.DictionaryObject()
#ocgs = PyPDF2.generic.ArrayObject()

##for i in inp.pages:
#i = inp.pages[0]
#page += 1
#template_page_size = i.mediaBox  
#op = PyPDF2.pdf.PageObject.createBlankPage(
  #width=template_page_size.getWidth(),
  #height=template_page_size.getHeight())  
#op[contentkey] = PyPDF2.generic.ArrayObject()
#op[resourcekey] = PyPDF2.generic.DictionaryObject()

#ocgname = PyPDF2.generic.NameObject('/oc%d' % page)
#ocgstart = PyPDF2.generic.DecodedStreamObject()
#ocgstart._data = "/OC %s BDC\n" % ocgname
#ocgend = PyPDF2.generic.DecodedStreamObject()
#ocgend._data = "EMC\n"
#if isinstance(i['/Contents'], PyPDF2.generic.ArrayObject):
  #i[PyPDF2.generic.NameObject('/Contents')].insert(0, ocgstart)
  #i[PyPDF2.generic.NameObject('/Contents')].append(ocgend)
#else:
  #i[PyPDF2.generic.NameObject(
      #'/Contents')] = PyPDF2.generic.ArrayObject((ocgstart, i['/Contents'], ocgend)) 

#op.mergePage(inp.getPage(0))

#ocg = PyPDF2.generic.DictionaryObject()
#ocg[PyPDF2.generic.NameObject(
    #'/Type')] = PyPDF2.generic.NameObject('/OCG')
#ocg[PyPDF2.generic.NameObject(
    #'/Name')] = PyPDF2.generic.TextStringObject('Layer %d' % (page + 1))
#indirect_ocg = o._addObject(ocg)
#properties[ocgname] = indirect_ocg
#ocgs.append(indirect_ocg)



#ocproperties = PyPDF2.generic.DictionaryObject()
#ocproperties[PyPDF2.generic.NameObject('/OCGs')] = ocgs
#defaultview = PyPDF2.generic.DictionaryObject()
#defaultview[PyPDF2.generic.NameObject(
  #'/Name')] = PyPDF2.generic.TextStringObject('Default')
#defaultview[PyPDF2.generic.NameObject(
  #'/BaseState ')] = PyPDF2.generic.NameObject('/ON ')
#defaultview[PyPDF2.generic.NameObject('/ON')] = ocgs
#if reverse_all_but_last:
  #defaultview[PyPDF2.generic.NameObject(
      #'/Order')] = PyPDF2.generic.ArrayObject(reversed(ocgs[:-1]))
  #defaultview[PyPDF2.generic.NameObject('/Order')].append(ocgs[-1])
#else:
  #defaultview[PyPDF2.generic.NameObject(
      #'/Order')] = PyPDF2.generic.ArrayObject(reversed(ocgs))
#defaultview[PyPDF2.generic.NameObject('/OFF')] = PyPDF2.generic.ArrayObject()

#ocproperties[PyPDF2.generic.NameObject('/D')] = o._addObject(defaultview)

#op[resourcekey][propertieskey] = o._addObject(properties)
##print(ocproperties)
#op.getObject()[PyPDF2.generic.NameObject('/OCProperties')] = o._addObject(ocproperties)
#o.addPage(op)
