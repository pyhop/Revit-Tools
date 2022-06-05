"""
Sample ImportInstance Selection in View
"""
__title__ = 'Select AutoCAD Similar Blocks'
__author__= 'marentette'

from Autodesk.Revit.DB import(FilteredElementCollector,
                                        BuiltInParameter,
                                        ElementId,
                                        ImportInstance)
from Autodesk.Revit.UI.Selection import(ObjectType,
                                        ISelectionFilter)
from System.Collections.Generic import List
from pyrevit import forms
from rpw import revit, db

doc = revit.doc
act_view = doc.ActiveView
uidoc = revit.uidoc

class AutoCAD_Filter(ISelectionFilter):
    def AllowElement(self, element):
        """
        Selection filter so the user can only pick
        a AutoCAD block
        """
        if element.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString() == "Import Symbol":
        	return True
        else:
        	return False
#Collect all import instances in view
importinstances = FilteredElementCollector(doc,act_view.Id) \
                                        .OfClass(ImportInstance) \
                                        .WhereElementIsNotElementType().ToElements()
#Using pyRevits warning bar, ask user to select AutoCAD block
message = "Select AutoCAD Block"
with forms.WarningBar(title=message):
    picked= uidoc.Selection.PickObject(ObjectType.Element, AutoCAD_Filter(), "Pick AutoCAD Block")
#Get Import Instance from Selection
symbol = doc.GetElement(picked)
#Get Symbol Name of Selection
name = symbol.get_Parameter(BuiltInParameter.IMPORT_SYMBOL_NAME).AsString()
#Collect all the blocks in view with the same name
similar_blocks = [i.Id for i in importinstances if \
            i.get_Parameter(BuiltInParameter.IMPORT_SYMBOL_NAME).AsString() == name]
#Select in View
uidoc.Selection.SetElementIds(List[ElementId](similar_blocks))
