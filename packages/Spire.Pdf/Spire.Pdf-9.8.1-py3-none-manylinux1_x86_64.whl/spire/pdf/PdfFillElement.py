from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFillElement (  PdfDrawWidget) :
    """
    <summary>
        Represents an element that could be drawn and/or filled.
    </summary>
    """
    @property

    def Brush(self)->'PdfBrush':
        """
    <summary>
        Gets or sets the brush.
    </summary>
        """
        GetDllLibPdf().PdfFillElement_get_Brush.argtypes=[c_void_p]
        GetDllLibPdf().PdfFillElement_get_Brush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFillElement_get_Brush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @Brush.setter
    def Brush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfFillElement_set_Brush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFillElement_set_Brush(self.Ptr, value.Ptr)

