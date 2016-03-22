
# Import arcpy module
import arcpy, os

# Script arguments
segmentations = arcpy.GetParameterAsText(0)
outputLocation = arcpy.GetParameterAsText(1)

# SQL Statements
forest_sql = '''
"CLASS_NAME"='Forest'
'''
union_sql = '''
"FID_forest_segments" = -1 AND "Shape_Area" < 1000
'''
impervious_sql = '''
"CLASS_NAME"='Impervious'
'''
not_forest = '''
"CLASS_NAME"='Low Vegetation' OR "CLASS_NAME"='Extra Vegetation' OR "CLASS_NAME"='Tilled Field' OR "CLASS_NAME"='Impervious'
'''
not_low_veg = '''
"CLASS_NAME"='Forest' OR "CLASS_NAME"='Impervious'
'''
not_impervious = '''
"CLASS_NAME"='Low Vegetation' OR "CLASS_NAME"='Extra Vegetation' OR "CLASS_NAME"='Tilled Field' OR "CLASS_NAME"='Forest'
'''

# Fill Forest Gaps
i=0
merge_layers = []
for layer in segmentations.split(';'):
    arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", forest_sql)
    arcpy.MakeFeatureLayer_management(layer, r"in_memory\selection" + str(i))
    merge_layers.append(r"in_memory\selection" + str(i))
    i+=1
arcpy.Merge_management(merge_layers, r"in_memory\forest_segments")
forest_union = arcpy.Union_analysis(r"in_memory\forest_segments", os.path.join(outputLocation, "forest_union"), "ONLY_FID", "", "NO_GAPS")
forest_union_layer = arcpy.MakeFeatureLayer_management(forest_union, os.path.join(outputLocation, "forest_union_layer"))
arcpy.SelectLayerByAttribute_management(forest_union_layer, "NEW_SELECTION", union_sql)
patch_speckles = arcpy.CopyFeatures_management(forest_union_layer, os.path.join(outputLocation, "patch_speckles"))

# Extract impervious segments
i=0
merge_layers = []
for layer in segmentations.split(';'):
    arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", impervious_sql)
    arcpy.MakeFeatureLayer_management(layer, r"in_memory\selection" + str(i))
    merge_layers.append(r"in_memory\selection" + str(i))
    i+=1
arcpy.Merge_management(merge_layers, os.path.join(outputLocation, "segments_impervious"))

# Create Patchers
patchers = [not_forest, not_low_veg, not_impervious]
for patcher in patchers:
    merge_layers = []
    i=0
    for layer in segmentations.split(';'):
        arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", patcher)
        arcpy.MakeFeatureLayer_management(layer, r"in_memory\selection" + str(i))
        merge_layers.append(r"in_memory\selection" + str(i))
        i+=1
    if len(patcher) == 126:
        forest = arcpy.Merge_management(merge_layers, os.path.join(outputLocation, "patcher_forest"))
        arcpy.CalculateField_management(forest, "CLASS_NAME", "'Forest'", "PYTHON")
    elif len(patcher) == 52:
        merge_layers.append(patch_speckles)
        low = arcpy.Merge_management(merge_layers, os.path.join(outputLocation, "patcher_low_vegetation"))
        arcpy.CalculateField_management(low, "CLASS_NAME", "'Low Vegetation'", "PYTHON")
    elif len(patcher) == 122:
        merge_layers.append(patch_speckles)
        impervious = arcpy.Merge_management(merge_layers, os.path.join(outputLocation, "patcher_impervious"))
        arcpy.CalculateField_management(impervious, "CLASS_NAME", "'Impervious'", "PYTHON")
