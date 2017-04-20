# from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
# from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from io import open
from io import StringIO


def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content


pdfFile = open('./笨方法学Python.PDF', 'rb')

outputString = readPDF(pdfFile)
print(outputString)
# outputFile = open('./笨方法学Python.txt', 'w')
# outputFile.write(outputString)

pdfFile.close()
# outputFile.close()

