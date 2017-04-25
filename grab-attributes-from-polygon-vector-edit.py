__author__ = 'Colin'

import arcpy

arcpy.env.overwriteOutput = True

parcel_file = r"\\Ccsvr01\d\GIS\NALCC\NALCC_Restoration_Tool_Workspace\HUC_12.gdb\HUC_12_Clipped"
parcel_layer = arcpy.MakeFeatureLayer_management(parcel_file, "parcel_layer")

# EDIT 1
chop_file = r"\\Ccsvr01\d\GIS\NALCC\NALCC_Restoration_Tool_Workspace\NEHUC8.shp"
chop_layer = arcpy.MakeFeatureLayer_management(chop_file, "chop_layer")

# EDIT 2
field = "HUC12"

# EDIT 3
fields = ["HUC8"]

with arcpy.da.SearchCursor(chop_file, fields) as cursor:
    for row in cursor:

        sql = '"HUC8" = ' + "'" + row[0] + "'"

        arcpy.AddMessage(sql)

        arcpy.SelectLayerByAttribute_management(chop_layer, "NEW_SELECTION", sql)

        current_chop_layer = arcpy.MakeFeatureLayer_management(chop_layer, "current_chop_layer")
        arcpy.SelectLayerByLocation_management(parcel_layer, "HAVE_THEIR_CENTER_IN", current_chop_layer, "", "NEW_SELECTION")

        # EDIT 5
        arcpy.CalculateField_management(parcel_layer, "HUC8", "'" + row[0] + "'", "Python")
