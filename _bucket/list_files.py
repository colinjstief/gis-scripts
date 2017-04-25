__author__ = 'cstief'

import os, sys

# Open a file
path = r"\\Ccsvr01\d\GIS\NALCC\NALCC_Restoration_Tool_Workspace\HUC_12_Tables"
dirs = os.listdir( path )

# This would print all the files and directories
for file in dirs:
   print file