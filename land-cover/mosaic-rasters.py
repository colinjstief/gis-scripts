##### Title: Rasters for Sub-watersheds
##### Author: Colin Stief

import arcpy, os

# Get reference to your dataframe
mxd = arcpy.mapping.MapDocument("CURRENT") 
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

# User specifies imagery folder and watershed feature
arcpy.env.workspace = arcpy.GetParameterAsText(0)
workspace = arcpy.env.workspace

i = 1

groups = arcpy.mapping.ListLayers(mxd, "", df)

for layer in groups:
	if layer.isGroupLayer and layer.name == "Mosaic":
		
		subLayerList = []
		for subLayer in layer:
			subLayerList.append(subLayer)
		outputName = "Mosaic_" + str(i) + ".tif"
		arcpy.MosaicToNewRaster_management(subLayerList, workspace, outputName, "", "", "" , 4, "", "")
		
		i += 1
	else:
		pass

arcpy.AddMessage("Complete!")		