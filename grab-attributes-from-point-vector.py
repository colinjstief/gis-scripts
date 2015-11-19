__author__ = 'Colin'

import arcpy

#primary_layer = arcpy.GetParameterAsText(0)
#unique_field = arcpy.GetParameterAsText(1)
#calculate_field = arcpy.GetParameterAsText(2)

#attribute_layer = arcpy.GetParameterAsText(3)
#grab_field = arcpy.GetParameterAsText(4)

primary_layer_raw = "\\\\Ccsvr01\\d\\GIS\\PG_County\\Fields.gdb\\Parcels_Gaps"
primary_layer = arcpy.MakeFeatureLayer_management(primary_layer_raw, "primary_layer")
attribute_layer = "\\\\Ccsvr01\\d\\GIS\\PG_County\\CleanDatasets\\additional_data\\GISDEV_WSHED_12.shp"

join_field = "TARGET_FID"
fields = [join_field, "DNR12DIG"]

values = {}

memory_join = "in_memory\\joined_features"
arcpy.SpatialJoin_analysis(primary_layer, attribute_layer, memory_join, "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "INTERSECT", "","")

rows = arcpy.da.SearchCursor(memory_join, fields)
for row in rows:
    target_fid = row[0]
    grab_attribute = row[1]

    if target_fid in values:
        attribute_list = values[target_fid]
        attribute_list.append(grab_attribute)
        values[target_fid] = attribute_list

    else:
        values[target_fid] = [grab_attribute]

for item in values:
    sql = "OBJECTID = " + str(item)
    #arcpy.AddMessage(sql)
    arcpy.SelectLayerByAttribute_management(primary_layer, "NEW_SELECTION", sql)
    list_string = "'" + ", ".join(values[item]) + "'"
    #arcpy.AddMessage(list_string)
    arcpy.CalculateField_management(primary_layer, "MD_Wat", list_string, "Python")

    arcpy.AddMessage("Finished with " + str(item))