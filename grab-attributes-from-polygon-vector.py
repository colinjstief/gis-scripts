__author__ = 'Colin'

import arcpy

arcpy.env.overwriteOutput = True

parcel_file = "\\\\Ccsvr01\\d\\GIS\\Lower_Susquehanna_Conservation_Toolbox\\Parcels.shp"
parcel_layer = arcpy.MakeFeatureLayer_management(parcel_file, "parcel_layer")

# EDIT 1
chop_file = "\\\\Ccsvr01\\d\\GIS\\Lower_Susquehanna_Conservation_Toolbox\\Soils.shp"
chop_layer = arcpy.MakeFeatureLayer_management(chop_file, "chop_layer")

# EDIT 2
field = "hydgrp"

# EDIT 3
fields = ["hydgrp"]
classes = ['A','A/D','B','B/D','C','C/D','D']

#rows = arcpy.da.SearchCursor(chop_file, fields)
#for row in rows:
for this_class in classes:

    value_raw = this_class
    sql = field + " = " + "'" + value_raw + "'"

    arcpy.AddMessage(sql)

    arcpy.SelectLayerByAttribute_management(chop_layer,"NEW_SELECTION", sql)

    current_chop_layer = arcpy.MakeFeatureLayer_management(chop_layer, "current_chop_layer")
    arcpy.SelectLayerByLocation_management(parcel_layer, "INTERSECT", current_chop_layer, "", "NEW_SELECTION")

    codeblock = """def grabValue(existingValue):
        if existingValue != "NA":
            newValue = existingValue + ", " + "%s"
            return newValue
        else:
            newValue = "%s"
            return newValue
    """ % (value_raw, value_raw)

    # EDIT 4
    expression = "grabValue(!SoilGrp!)"

    # EDIT 5
    arcpy.CalculateField_management(parcel_layer, "SoilGrp", expression, "Python", codeblock)