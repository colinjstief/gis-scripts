__author__ = 'Colin'

import arcpy

#primary_layer = arcpy.GetParameterAsText(0)
#attribute_layer = arcpy.GetParameterAsText(1)
#fields = arcpy.GetParameterAsText(2)
primary_layer_raw = "\\\\Ccsvr01\\d\\GIS\\PG_County\\Fields.gdb\\Parcels_Gaps"
primary_layer = arcpy.MakeFeatureLayer_management(primary_layer_raw, "primary_layer")
attribute_layer = "\\\\Ccsvr01\\d\\GIS\\PG_County\\CleanDatasets\\additional_data\\bmps.mdb\\bmps\\bmps"

fields = ["TARGET_FID", "STRU_NO"]

values = {}

#memory_join = "\\\\Ccsvr01\\d\\GIS\\PG_County\\Fields.gdb\\joined_features
memory_join = "in_memory\\joined_features"
arcpy.SpatialJoin_analysis(primary_layer, attribute_layer, memory_join, "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "INTERSECT", "","")
rows = arcpy.da.SearchCursor(memory_join, fields)
for row in rows:
    target_fid = row[0]
    bmp_id = row[1]

    if target_fid in values:
        bmp_list = values[target_fid]
        bmp_list.append(bmp_id)
        values[target_fid] = bmp_list

    else:
        values[target_fid] = [bmp_id]

for item in values:
    sql = "OBJECTID = " + str(item)
    arcpy.SelectLayerByAttribute_management(primary_layer, "NEW_SELECTION", sql)
    list_string = "'" + ", ".join(values[item]) + "'"
    arcpy.CalculateField_management(primary_layer, "BMP_ID", list_string, "Python")

    arcpy.AddMessage("Finished with " + str(item))