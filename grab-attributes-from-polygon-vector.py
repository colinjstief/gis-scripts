__author__ = 'Colin'

import arcpy

arcpy.env.overwriteOutput = True

parcel_file = "\\\\Ccsvr01\\d\\GIS\\PG_County\\Fields.gdb\\Parcels_Gaps"
parcel_layer = arcpy.MakeFeatureLayer_management(parcel_file, "parcel_layer")

# EDIT 1
chop_file = "\\\\Ccsvr01\\d\\GIS\\PG_County\\CleanDatasets\\storm_drain_inventory\\Structures_SD_Type_Dissolve_MP_Remaining.shp"
chop_layer = arcpy.MakeFeatureLayer_management(chop_file, "chop_layer")

# EDIT 2
field = "StrType"

# EDIT 3
fields = ["StrType"]

rows = arcpy.da.SearchCursor(chop_file, fields)
for row in rows:
#codes = [1,2,3,4,5,6]

#for code in codes:
    #value_raw = code
    #value_string = str(code)
    value_raw = row[0]
    #value = value_raw.lstrip("0")
    sql = field + " = " + "'" + value_raw + "'"
    #sql = field + " = " + str(value_raw)

    #value_stripped_unicode = value.lstrip("0")
    #value = value_raw.encode("utf-8")
    #value_stripped = "'" + value_stripped_string + "'"

    arcpy.AddMessage(sql)

    arcpy.SelectLayerByAttribute_management(chop_layer,"NEW_SELECTION", sql)

    current_chop_layer = arcpy.MakeFeatureLayer_management(chop_layer, "current_chop_layer")
    arcpy.SelectLayerByLocation_management(parcel_layer, "HAVE_THEIR_CENTER_IN", current_chop_layer, "", "NEW_SELECTION")

    codeblock = """def grabValue(existingValue):
        if existingValue != "NA":
            newValue = existingValue + ", " + "%s"
            return newValue
        else:
            newValue = "%s"
            return newValue
    """ % (value_raw, value_raw)

    # EDIT 4
    expression = "grabValue(!StrType!)"

    # EDIT 5
    arcpy.CalculateField_management(parcel_layer, "StrType", expression, "Python", codeblock)