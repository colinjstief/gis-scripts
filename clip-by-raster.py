##### Title: Clip by Raster Extent
##### Author: Colin Stief

import arcpy, os

## Grab user inputs
feature = arcpy.GetParameterAsText(0)
raster = arcpy.GetParameterAsText(1)
arcpy.env.workspace = arcpy.GetParameterAsText(2)
output_feature_name = arcpy.GetParameterAsText(3)

## Make new array to hold extent, then grab it from raster
pnt_array = arcpy.Array()
extent = arcpy.Raster(raster).extent
pnt_array.add(extent.lowerLeft)
pnt_array.add(extent.lowerRight)
pnt_array.add(extent.upperRight)
pnt_array.add(extent.upperLeft)

## Create new polygon from extent
poly = arcpy.Polygon(pnt_array)

## Perform Clip
arcpy.Clip_analysis(feature, poly, output_feature_name)




