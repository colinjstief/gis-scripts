## group segmentation files
## colin stief
## february 18, 2016

import arcpy, csv, os

### Running counts
i = 0
k = 1

### Files and Folders

county = "Tioga"
workspace = "\\\\CCSVR01\\EastWalk\\Segmentation"
segmentation_folder = os.path.join(workspace, county)

geodatabase_name = county + ".gdb"
geodatabase = os.path.join(workspace, geodatabase_name)

### In_memory lists
dissolve_list = []
merge_list = []

### Procedure

# Loop through segmentation folder
for root, dirs, files in os.walk(segmentation_folder, topdown=True):
    for name in files:
        if name[name.rfind("."):len(name)] == ".shp":

            # Dissolve segmentation
            input_file = os.path.join(root, name)
            output_file = os.path.join("in_memory", name[:-4])

            output_dissolve = arcpy.Dissolve_management(input_file, output_file)

            # Add field and populate it with the file name
            arcpy.AddField_management(output_dissolve, "file_name", 'text')
            arcpy.CalculateField_management(output_dissolve, 'file_name', '"' + name[:-4] + '"')

            dissolve_list.append(output_dissolve)

            i+=1

            print "Finished with vector " + str(i)

            if i == 1000:
                merge_name = "Merge_" + str(k)
                partial_merge = os.path.join(geodatabase, merge_name)
                arcpy.Merge_management(dissolve_list, partial_merge)
                merge_list.append(partial_merge)

                k+=1

                arcpy.Delete_management("in_memory")
                dissolve_list = []

            elif i == 2000:
                merge_name = "Merge_" + str(k)
                partial_merge = os.path.join(geodatabase, merge_name)
                arcpy.Merge_management(dissolve_list, partial_merge)
                merge_list.append(partial_merge)

                k+=1

                arcpy.Delete_management("in_memory")
                dissolve_list = []

            elif i == 2494:
                merge_name = "Merge_" + str(k)
                partial_merge = os.path.join(geodatabase, merge_name)
                arcpy.Merge_management(dissolve_list, partial_merge)
                merge_list.append(partial_merge)

                k+=1

                arcpy.Delete_management("in_memory")
                dissolve_list = []

complete_merge = os.path.join(geodatabase, "Complete_Merge")
arcpy.Merge_management(merge_list, complete_merge)