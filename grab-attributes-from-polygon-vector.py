__author__ = 'Colin'

import arcpy

arcpy.env.overwriteOutput = True

parcel_file = "\\\\Ccsvr01\\d\\GIS\\PG_County\\Fields.gdb\\Parcels_Gaps"
parcel_layer = arcpy.MakeFeatureLayer_management(parcel_file, "parcel_layer")

chop_file = "\\\\Ccsvr01\\d\\GIS\\PG_County\\CleanDatasets\\additional_data\\GISDEV_WSHED_12.shp"
chop_layer = arcpy.MakeFeatureLayer_management(chop_file, "chop_layer")

fields = ["DNR12DIG"]

total_count = 0

rows = arcpy.da.SearchCursor(chop_file, fields)
for row in rows:

    huc = row[0]
    huc_stripped = huc.lstrip("0")
    sql = "DNR12DIG = " + "'" + huc + "'"
    print sql

    arcpy.SelectLayerByAttribute_management(chop_layer,"NEW_SELECTION", sql)

    current_chop_layer = arcpy.MakeFeatureLayer_management(chop_layer, "current_chop_layer")
    arcpy.SelectLayerByLocation_management(parcel_layer, "INTERSECT", current_chop_layer)

    codeblock = """def grabValue(existingValue):

        arcpy.AddMessage(existingValue)

        if existingValue != "":
            newValue = existingValue + ", " + %s
            return newValue

        else:
            newValue = %s
            return newValue
    """ % (huc_stripped, huc_stripped)

    expression = "grabValue(str(!MD_Wat!))"
    arcpy.CalculateField_management(parcel_layer, "MD_Wat", expression, "Python", codeblock)