## group segmentation files
## colin stief
## february 18, 2016

import arcpy, csv, os

### Files and Folders

county = "Tioga"
workspace = "\\\\CCSVR01\\EastWalk\\Segmentation"
segmentation_folder = os.path.join(workspace, county)
#arcpy.env.workspace = "\\\\CCSVR01\\Extra_GIS_Data\\NY_LeafOff\\By_County_and_Year\\" + county + "\\Ortho_2015"

raster_count = list(range(1,2496))
#raster_list = arcpy.ListRasters("*","JP2")
#print len(raster_list)
i=0
# Loop through segmentation folder
for root, dirs, files in os.walk(segmentation_folder, topdown=True):
    for name in files:
        if name[name.rfind("."):len(name)] == ".shp":
            i+=1
            # Get Missing Tiles
            name_number = name[7:name.rfind(".")]
            number = int(name_number)

            if number in raster_count:
                raster_count.remove(number)

print str(i)