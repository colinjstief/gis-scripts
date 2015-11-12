
# Import arcpy module
import arcpy

# Script arguments
segmentations = arcpy.GetParameterAsText(0)
outputLocation = arcpy.GetParameterAsText(1)

classList = []
classList.append("Low Vegetation")
classList.append("Managed")
classList.append("Extra Vegetation")
classList.append("Tilled Field")
classList.append("Impervious")
classList.append("Water")
classList.append("Crop")
classList.append("Ag")
classList.append("Forest")
classList.append("Unclassified")
classList.append("Masked")
classList.append("Bare Earth")
classList.append("Non-Agriculture Vegetation")

for landClass in classList:
	
	mergeLayers = []
	toggle = "false"
	print "toggle set to " + toggle
	
	expression = '"CLASS_NAME" =' + "'" + landClass + "'"
	arcpy.AddMessage(expression)
	
	for layer in segmentations.split(';'):
		arcpy.AddMessage(layer)
		arcpy.SelectLayerByAttribute_management(layer, "ADD_TO_SELECTION", expression)
		count = int(arcpy.GetCount_management(layer).getOutput(0))
		if count > 0:
			toggle = "true"
			mergeLayers.append(layer)
	
	if toggle == "true":
		if landClass == "Non-Agriculture Vegetation":
			output = outputLocation + "/merge_non_ag_veg"
		else:
			output = outputLocation + "/merge_" + landClass
		arcpy.Merge_management(mergeLayers, output, "")
	
	for layer in segmentations.split(';'):
		arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")
	
	