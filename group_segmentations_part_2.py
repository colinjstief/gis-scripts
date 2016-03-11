## group segmentation files
## colin stief
## february 18, 2016

import arcpy, csv, os

### Running counts
j = 1

### Files and Folders

county = "Tioga"
workspace = "\\\\CCSVR01\\EastWalk\\Segmentation"
segmentation_folder = os.path.join(workspace, county)

geodatabase_name = county + ".gdb"
geodatabase = os.path.join(workspace, geodatabase_name)

grid_file = os.path.join(workspace, geodatabase_name, "Fishnet")
grid_layer = arcpy.MakeFeatureLayer_management(grid_file, "grid_layer")

### Procedure

complete_merge = os.path.join(geodatabase, "Complete_Merge")
complete_merge_layer = arcpy.MakeFeatureLayer_management(complete_merge, "complete_merge_layer")

with arcpy.da.SearchCursor(grid_file, ("OID@")) as cursor:
    for row in cursor:

        current_group_list = []

        sql = "OID = " + str(row[0])
        arcpy.SelectLayerByAttribute_management(grid_layer,"NEW_SELECTION", sql)
        current_cell = arcpy.MakeFeatureLayer_management(grid_layer, "current_cell")

        arcpy.SelectLayerByLocation_management(complete_merge_layer, "HAVE_THEIR_CENTER_IN", current_cell, "", "NEW_SELECTION")

        with arcpy.da.SearchCursor(complete_merge_layer, "file_name") as innerCursor:
            for innerRow in innerCursor:
                current_file_name = innerRow[0] + ".shp"
                current_file_path = os.path.join(segmentation_folder, current_file_name)
                current_group_list.append(current_file_path)

        if len(current_group_list) > 0:

            current_group_name = "Group_" + str(j)
            current_group_layer = os.path.join(geodatabase, current_group_name)

            current_group_footprint_name = current_group_name + "_Footprint"
            current_group_footprint = os.path.join(geodatabase, current_group_footprint_name)

            field_map = arcpy.FieldMappings()
            for part in current_group_list:
                field_map.addTable(part)

            for field in field_map.fields:
                if field.name not in ["REGION_ID"]:
                    field_map.removeFieldMap(field_map.findFieldMapIndex(field.name))

            arcpy.Merge_management(current_group_list, current_group_layer, field_map)
            #arcpy.Dissolve_management(current_group_layer, current_group_footprint)
            print "Added Group " + str(j) + " to the geodatabase."
            j += 1

        arcpy.Delete_management(current_cell)