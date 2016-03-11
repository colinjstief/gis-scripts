## batch fill/dir/acc
## colin stief
## february 12, 2016

import arcpy, csv, os, shutil

# Folder of rasters
root = "\\\\CCSVR01\\d\\GIS\\Lower_Susquehanna_Conservation_Toolbox\\Watershed_Data\\"
dem_mosaic = root + "WatershedDelineator.gdb\\DEM"

workspace = root + "Colins_Workspace\\"
dem_folder = workspace + "Split_DEMs"
huc_shapefile = workspace + "Area_HUC_10s_Projected.shp"
huc_layer = arcpy.MakeFeatureLayer_management(huc_shapefile, "huc_layer")

with arcpy.da.SearchCursor(huc_shapefile, ("HUC_10","HU_10_Name")) as cursor:
    for row in cursor:

        output_raster = dem_folder  + "\\HUC_" + row[0] + ".tif"
        sql = "HUC_10 = " + "'" + row[0] + "'"
        arcpy.SelectLayerByAttribute_management(huc_layer,"NEW_SELECTION", sql)
        arcpy.Clip_management(dem_mosaic, "291701.880996553 4347511.17240114 456405.595565103 4491625.99990179", output_raster, huc_layer, "-3.402823e+038", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

        print "Finished clipping HUC " + row[0]
