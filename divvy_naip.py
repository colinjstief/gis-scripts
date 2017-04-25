## divvy naip tiles to local drive
## colin stief
## march 10, 2016

# Libraries
import os, glob, shutil, itertools

# Directories
tile_folder = r"\\Ccsvr01\d\GIS\Conservation_Innovation\Classification_Resources\StaffFolders\Colin\Randolph"
local_folder = r"C:\Users\ChesConserv1\Desktop\Colin_GIS\Randolph"
folder_prefix = "Randolph"

# Get files as list
os.chdir(tile_folder)
tiles = glob.glob('*.j*')

print "There are " + str(len(tiles)) + " tiles in this folder."

# Grouping function
def groupFunction(tiles, magic_number):
    iterator = iter(tiles)
    while True:
        items = list(itertools.islice(iterator, magic_number))
        if len(items) == 0:
            break
        yield items

for group_number, group in enumerate(groupFunction(tiles, 375)):
    folder_name = folder_prefix + str(group_number)
    folder_path = os.path.join(local_folder, folder_name)
    print "Moving files into: " + folder_path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for tile in group:
        shutil.copy(tile, folder_path)

print "Finished."