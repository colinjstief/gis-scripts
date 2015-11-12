##### Title: Rasters for Sub-watersheds
##### Author: Colin Stief

import arcpy, os

# Get reference to your dataframe
mxd = arcpy.mapping.MapDocument("CURRENT") 
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

# User specifies imagery folder and watershed feature
arcpy.env.workspace = arcpy.GetParameterAsText(0)
featureInput = arcpy.GetParameterAsText(1)

i = 0

# Make sure that a single feature boundary is selected
# (Optional) Restrict Number of Selected Watersheds
# len(arcpy.Describe(featureInput).fidSet.split(";")) == 1
if str(arcpy.Describe(featureInput).fidSet.split(";")) != "[u'']":
	
	feature = arcpy.mapping.Layer(featureInput)
	featureExtent = feature.getSelectedExtent(True)
	
	try:
		# Loop through the rasters
		allImagery = arcpy.ListRasters()
		for image in allImagery:	
				
			desc = arcpy.Describe(image)	
			imageExtent = desc.extent
			
			if (featureExtent.overlaps(imageExtent) == True or
				featureExtent.within(imageExtent) == True or
				featureExtent.contains(imageExtent) == True):
		
				# Create Temporary Layer
				outputName = desc.file + str(i)
				arcpy.AddMessage(arcpy.env.workspace)
				arcpy.AddMessage(outputName)
				try:
					result = arcpy.MakeRasterLayer_management(image, outputName)
					imageLayer = result.getOutput(0)
					
					# Add Layer
					arcpy.mapping.AddLayer(df, imageLayer, "BOTTOM")
					
				except:
					arcpy.AddError(arcpy.GetMessages(2))
					
				i += 1
			else:
				pass

	except:
		arcpy.AddError(arcpy.GetMessages(2))

else:
	arcpy.AddError("Please make sure your feature is loaded into the table of contents, and that you select a single watershed boundary")
	
	