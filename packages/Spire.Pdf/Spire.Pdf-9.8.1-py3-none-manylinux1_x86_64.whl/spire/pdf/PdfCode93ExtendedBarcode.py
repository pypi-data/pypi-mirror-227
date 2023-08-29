from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCode93ExtendedBarcode (  PdfCode93Barcode) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfCode93ExtendedBarcode_CreatePdfCode93ExtendedBarcode.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCode93ExtendedBarcode_CreatePdfCode93ExtendedBarcode()
        super(PdfCode93ExtendedBarcode, self).__init__(intPtr)

    @dispatch
    def __init__(self, text:str):
        GetDllLibPdf().PdfCode93ExtendedBarcode_CreatePdfCode93ExtendedBarcodeT.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfCode93ExtendedBarcode_CreatePdfCode93ExtendedBarcodeT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCode93ExtendedBarcode_CreatePdfCode93ExtendedBarcodeT(text)
        super(PdfCode93ExtendedBarcode, self).__init__(intPtr)
    """
    <summary>
        Represents a code93 extended barcode.
    </summary>
<remarks> All 128 ASCII characters can be encoded in an extended Code 93 barcode. </remarks>
    """
