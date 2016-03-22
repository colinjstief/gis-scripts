## calculate field by file name
## colin stief
## march 10, 2016

# Libraries
import arcpy, os

feature = arcpy.GetParameter(0)
front_chop = int(arcpy.GetParameterAsText(1))
back_chop = -int(arcpy.GetParameterAsText(2))
field = arcpy.GetParameterAsText(3)

feature_details = arcpy.Describe(feature)
if back_chop == 0:
    value = feature_details.name[front_chop:]
else:
    value = feature_details.name[front_chop:back_chop]

arcpy.CalculateField_management(feature, field, '"' + value + '"', "PYTHON")

arcpy.AddMessage("Done")