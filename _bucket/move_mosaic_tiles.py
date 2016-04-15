## copy and move files
## colin stief
## february 3, 2016

import arcpy, csv, os, shutil

# Tile directory
tile_directory = r"\\CCSVR01\Extra_GIS_Data\NY_LeafOff\By_County_and_Year\Tioga\Ortho_2014"

# Destination
destination_directory = r"\\Ccsvr01\d\GIS\Conservation_Innovation\Classification_Resources\StaffFolders\Kathryn\Outputs"

# Make list of duplicates from Spreadsheet
spreadsheet_location = r"C:\Users\ChesConserv1\Desktop\Colin_GIS\_Bucket\Tioga_leafoff.csv"
spreadsheet = open(spreadsheet_location, 'rU')

tiles = []

for row in spreadsheet.readlines():
    tiles.append(row.strip())

i=0

for root, dirs, files in os.walk(tile_directory, topdown=True):
    for name in files:
        if (name[0:-4] in tiles and name[name.rfind("."):len(name)] == ".jp2"):
            current_location = os.path.join(root, name)
            destination = os.path.join(destination_directory, name)
            shutil.copy(current_location, destination)
            print "Copied " + name
            i+=1

print "Successfully moved " + str(i) + " files."