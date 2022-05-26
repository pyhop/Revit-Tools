"""
This script deletes sections that are not pinned or on sheets
"""
from Autodesk.Revit.DB import(
FilteredElementCollector,
View,
Viewport,
ViewType
)
from rpw import revit, db

__title__="Delete Unused Sections"
__author__ = "marentette"

doc = revit.doc

def sections_not_on_sheet(doc):
    """
    returns a list of sections that are not on sheets
    """
    viewports = FilteredElementCollector(doc) \
                .OfClass(Viewport).WhereElementIsNotElementType() \
                .ToElements()

    views = FilteredElementCollector(doc) \
                .OfClass(View).WhereElementIsNotElementType() \
                .ToElements()

    return [view for view in views \
            if not any(view.Id == viewport.ViewId for viewport in viewports) \
            and view.ViewType == ViewType.Section]

def section_pinned(doc, view):
    """
    returns True if any dependent elements are pinned. 
    """
    for elementId in view.GetDependentElements(None):
        element = doc.GetElement(elementId)
        if element.Pinned:
            return True
    return False

if __name__ == "__main__":
    with db.Transaction("Delete Unused Sections"):
        for section in sections_not_on_sheet(doc):
            if not section_pinned(doc,section):
                doc.Delete(section.Id)
