import arcpy

layer = arcpy.GetParameterAsText(0)
field_type = arcpy.GetParameterAsText(1)
avoid_fields = arcpy.GetParameterAsText(2)
raw_value = arcpy.GetParameterAsText(3)

fields = arcpy.ListFields(layer, "", field_type)

for field in fields:

	if field.name in avoid_fields:
		arcpy.AddMessage("Skipping: " + field.name)
	else:
		if field_type == "String":
			value = "'" + raw_value + "'"
		if field_type == "Integer":
			value = int(raw_value)
		if field_type == "Float":
			value = float(raw_value)

		arcpy.CalculateField_management(layer, field.name, value, "Python")
		arcpy.AddMessage("Finished updating: " + field.name)