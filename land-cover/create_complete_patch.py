
# Import arcpy module
import arcpy, os

# Parameters
update_list = arcpy.GetParameter(0)
output_raster = arcpy.GetParameterAsText(1)

# Loop through list of files
count = len(update_list)
i=1

for layer in update_list:
	if i==1:
		input_layer = layer
		i+=1
	elif i < count:
		update_layer = layer
		temp_name = "temp_" + str(i)
		temp_layer = os.path.join("in_memory", temp_name)
		arcpy.Update_analysis(input_layer, update_layer, temp_layer, "BORDERS", "")
		arcpy.AddMessage(temp_name)
		input_layer = temp_layer
		i+=1
	else:
		update_layer = layer
		final_update = arcpy.Update_analysis(input_layer, update_layer, "in_memory\\final_update", "BORDERS", "")

arcpy.PolygonToRaster_conversion(final_update, "CLASS_NAME", output_raster, "", "", 1)

arcpy.AddMessage("Finished")