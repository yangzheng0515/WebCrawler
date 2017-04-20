from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams 
from pdfminer.converter import PDFPageAggregator

#
#来自慕课网 http://www.imooc.com/video/12635
#惨遭失败，以后再试试
#解析pdf文档：pdfminer3k
#pip install pdfminer3k

fp = open('Scrapy中文指南.pdf', 'rb')
# 创建一个文档关联的解释器
parser = PDFParser(fp)
# PDF文档的对象
doc = PDFDocument()
# 链接解释器和文档
parser.set_document(doc)
doc.set_parser(parser)
# 初始化文档
doc.initialize('')
#创建PDF资源管理器
resource = PDFResourceManager()
# 参数解析器
laparam = LAParams()
# 创建一个聚合器
device = PDFPageAggregator()
# 创建PDF页面解释器
interpreter = PDFPageInterpreter(resource, device)
# 使用文档对象得到页面的集合
for page in doc.get_pages():
# 使用页面解释器来读取
interpreter.process_page(page)
# 使用聚合器来获得内容
layout = device.get_result()

for out in layout:
	if hasattr(out, 'get_text'):
	    print(out.get_text())

