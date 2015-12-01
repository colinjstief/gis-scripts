__author__ = 'Colin'

import arcpy

arcpy.env.overwriteOutput = True

parcel_file = "\\\\Ccsvr01\\d\\GIS\\PG_County\\Fields.gdb\\Parcels_Gaps"
parcel_layer = arcpy.MakeFeatureLayer_management(parcel_file, "parcel_layer")

# EDIT 1
chop_file = "\\\\Ccsvr01\\d\\GIS\\PG_County\\CleanDatasets\\storm_drain_inventory\\Pipes_Dissolve_SD_Size_Type.shp"
chop_layer = arcpy.MakeFeatureLayer_management(chop_file, "chop_layer")

# EDIT 2
field = "SD_T_S1_S2"

# EDIT 3
fields = ["SD_T_S1_S2"]

uniquePipes = set([row.getValue(field) for row in arcpy.SearchCursor(chop_layer)])

for pipe in uniquePipes:

    value_raw = pipe
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
    expression = "grabValue(!PipeType!)"

    # EDIT 5
    arcpy.CalculateField_management(parcel_layer, "PipeType", expression, "Python", codeblock)