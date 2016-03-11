## remove duplicate naip
## colin stief
## february 3, 2016

import arcpy, csv, os, shutil

# Tile directory
tile_directory = r"\\CCSVR01\Extra_GIS_Data\GIS\LeafOffClassification\DataDownload"

# Destination
destination_directory = r"\\CCSVR01\EastWalk\NAIP\Caroline"

# Make list of duplicates from Spreadsheet
spreadsheet_location = r"C:\Users\ChesConserv1\Desktop\Colin_GIS\_Bucket\caroline_rasters.csv"
spreadsheet = open(spreadsheet_location, 'rU')

tiles = []

for row in spreadsheet.readlines():
    tiles.append(row.strip())

i=0
#exclude = set(["NAIP_LeafOff_By_County_and_Year"])

for root, dirs, files in os.walk(tile_directory, topdown=True):
    #dirs[:] = [d for d in dirs if d not in exclude]
    for name in files:
        if (name[0:-4] in tiles and name[name.rfind("."):len(name)] == ".jp2"):
            current_location = os.path.join(root, name)
            destination = os.path.join(destination_directory, name)
            #shutil.move(current_location, destination)
            shutil.copy(current_location, destination)
            print "Copied " + name
            i+=1

print "Successfully moved " + str(i) + " files."