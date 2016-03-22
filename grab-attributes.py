# author: conor
# 3/16/16

import arcpy
arcpy.env.overwriteOutput = True

# Shapefiles and layers

unit_file = r"\\Ccsvr01\d\GIS\York\York_Bayfast_App_Workspace\York_Bayfast_App\Data_Web_Projected.gdb\York_Parcels"
units = arcpy.MakeFeatureLayer_management(unit_file, "units")

attribute_file = r"\\Ccsvr01\d\GIS\York\York County\bndry.shp"
attributes = arcpy.MakeFeatureLayer_management(attribute_file, "attributes")

# Loop through the HUC
rows = arcpy.da.SearchCursor(attribute_file, ["Label"])
for row in rows:

    # Make temporary layer of only the current HUC
    current_attribute = row[0]
    sql = '"Label" =' + "'" + current_attribute + "'"
    arcpy.SelectLayerByAttribute_management(attributes, "NEW_SELECTION", sql)
    current_attribute_layer = arcpy.MakeFeatureLayer_management(attributes, "current_attribute_layer")

    # Select by location based on current huc
    arcpy.SelectLayerByLocation_management(units, "HAVE_THEIR_CENTER_IN", current_attribute_layer, "", "NEW_SELECTION")

    # Calculate field with current huc name
    arcpy.CalculateField_management(units, "Muni", '"' + row[0] + '"', "Python")

    arcpy.AddMessage("Finished with " + row[0])