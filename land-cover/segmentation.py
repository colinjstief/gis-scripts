import arcpy, os, sys

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

path = "C:\\Users\\Duncan\\Desktop\\_bucket\\GIS\\_Conservancy"
for root, dirs, files in os.walk(path):
    for dir in dirs:
        currentDir = os.path.join(root,dir)
		segments = []
        for sr, sd, sf in os.walk(currentDir):
            for file in sf:
                if file.endswith(".shp"):
                    currentFile = os.path.join(sr, file)
					segments.append(currentFile)
					if file.name = "segmentation1.shp":
						values = unique_values(currentFile, "CLASS_NAME")
						print values
		classList = []
		
			
for landClass in classList:

	expression = '"CLASS_NAME" =' + "'" + landClass + "'"
	arcpy.AddMessage(expression)
	
	for layer in segmentations.split(';'):
		arcpy.AddMessage(layer)
		arcpy.SelectLayerByAttribute_management(layer, "ADD_TO_SELECTION", expression)
		
	output = outputLocation + "/merge_" + landClass
	arcpy.Merge_management(segmentations, output, "")
	
	for layer in segmentations.split(';'):
		arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")