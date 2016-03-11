## remove duplicate naip
## colin stief
## february 3, 2016

import arcpy, csv, os, shutil

# NAIP Directory
naip_directory = r"\\CCSVR01\Extra_GIS_Data\GIS\LeafOffClassification\DataDownload"

# County and path
county = "Tompkins"
county_directory = "\\\\CCSVR01\\Extra_GIS_Data\\NY_LeafOff\\NAIP_LeafOff_By_County_and_Year\\" + county

# Make list of duplicates from Spreadsheet
tiles = []
directory = "\\\\CCSVR01\\Extra_GIS_Data\\NY_LeafOff\\NAIP_LeafOff_By_County_and_Year\\_Spreadsheets"
file = county + ".csv"
spreadsheet_location = directory + "\\" + file
spreadsheet = open(spreadsheet_location, 'rU')

for row in spreadsheet.readlines():
    tiles.append(row.strip())

i=0
exclude = set(["NAIP_LeafOff_By_County_and_Year"])

for root, dirs, files in os.walk(naip_directory, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for name in files:
        if name[0:-4] in tiles:
            current_location = os.path.join(root, name)
            destination = os.path.join(county_directory, name)
            shutil.move(current_location, destination)
            print "Moved " + name
            i+=1

print "Successfully moved " + str(i) + " files."