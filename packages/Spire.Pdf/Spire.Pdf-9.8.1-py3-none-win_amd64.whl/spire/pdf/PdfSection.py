from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSection (  IEnumerable) :
    """
    <summary>
        Represents a section entity. A section it's a set of the pages with similar page settings.
    </summary>
    """
    @property

    def Pages(self)->'PdfSectionPageCollection':
        """
    <summary>
        Gets the pages.
    </summary>
        """
        GetDllLibPdf().PdfSection_get_Pages.argtypes=[c_void_p]
        GetDllLibPdf().PdfSection_get_Pages.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSection_get_Pages(self.Ptr)
        ret = None if intPtr==None else PdfSectionPageCollection(intPtr)
        return ret


    @property

    def PageSettings(self)->'PdfPageSettings':
        """
    <summary>
        Gets or sets page settings of the section.
    </summary>
        """
        GetDllLibPdf().PdfSection_get_PageSettings.argtypes=[c_void_p]
        GetDllLibPdf().PdfSection_get_PageSettings.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSection_get_PageSettings(self.Ptr)
        ret = None if intPtr==None else PdfPageSettings(intPtr)
        return ret


    @PageSettings.setter
    def PageSettings(self, value:'PdfPageSettings'):
        GetDllLibPdf().PdfSection_set_PageSettings.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSection_set_PageSettings(self.Ptr, value.Ptr)

    @property

    def Template(self)->'PdfSectionTemplate':
        """
    <summary>
        Gets or sets a template for the pages in the section.
    </summary>
        """
        GetDllLibPdf().PdfSection_get_Template.argtypes=[c_void_p]
        GetDllLibPdf().PdfSection_get_Template.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSection_get_Template(self.Ptr)
        ret = None if intPtr==None else PdfSectionTemplate(intPtr)
        return ret


    @Template.setter
    def Template(self, value:'PdfSectionTemplate'):
        GetDllLibPdf().PdfSection_set_Template.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSection_set_Template(self.Ptr, value.Ptr)

    @property

    def Document(self)->'PdfDocumentBase':
        """
    <summary>
        Gets the owner document.
    </summary>
<value>The document.</value>
        """
        GetDllLibPdf().PdfSection_get_Document.argtypes=[c_void_p]
        GetDllLibPdf().PdfSection_get_Document.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSection_get_Document(self.Ptr)
        ret = None if intPtr==None else PdfDocumentBase(intPtr)
        return ret



    def add_PageAdded(self ,value:'PageAddedEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfSection_add_PageAdded.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSection_add_PageAdded(self.Ptr, intPtrvalue)


    def remove_PageAdded(self ,value:'PageAddedEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfSection_remove_PageAdded.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfSection_remove_PageAdded(self.Ptr, intPtrvalue)


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibPdf().PdfSection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibPdf().PdfSection_GetEnumerator.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSection_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret



    def LoadFromHTML(self ,url:str,enableJavaScript:bool,enableHyperlinks:bool,layoutFormat:'PdfHtmlLayoutFormat')->'PdfLayoutHTMLResult':
        """
    <summary>
        Draws HTML to PDF
    </summary>
    <param name="url">Url address</param>
    <param name="enableJavaScript">Enable javascrpit</param>
    <param name="enableHyperlinks">Enable hyperlink</param>
    <param name="layoutFormat">Layouts html view format</param>
        """
        intPtrlayoutFormat:c_void_p = layoutFormat.Ptr

        GetDllLibPdf().PdfSection_LoadFromHTML.argtypes=[c_void_p ,c_wchar_p,c_bool,c_bool,c_void_p]
        GetDllLibPdf().PdfSection_LoadFromHTML.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSection_LoadFromHTML(self.Ptr, url,enableJavaScript,enableHyperlinks,intPtrlayoutFormat)
        ret = None if intPtr==None else PdfLayoutHTMLResult(intPtr)
        return ret


