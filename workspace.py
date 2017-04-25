# Import libraries
import os, numpy as np, pandas as pd, scipy, openpyxl

# Set working directory
path = r"\\Ccsvr01\d\GIS\Envision James\SWCD Toolboxes\Tabulate_areas"
os.chdir( path )

# Identify specific tables
parcels = pd.read_excel( "parcel_info_area.xlsx" )

# Loop through directory
for root, dirs, files, in os.walk( path ):
    for name in files:
        if ( name[name.rfind("."):len(name)] == "xlsx" ) and ( name != "parcel_info_area.xlsx" ):

            # Open each table
            table = pd.read_excel( os.path.join(root, name) )

            # Merge tables
            parcels = parcels.merge(table, how="left", on='Unique_ID')

# Export to excel
parcels.to_csv("parcel_buffer_area.csv")