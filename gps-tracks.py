## gps tracks
## colin stief
## december 17, 2014

import arcpy, csv, os

#### Python Portion

## Setup spreadsheet file
output_location = "C:\Users\Duncan\Desktop\gps_tracks"
spreadsheet_name = "canada_database_ira.csv"
spreadsheet_location = output_location + "\\" + spreadsheet_name
spreadsheet = open(spreadsheet_location, 'rU')
tracks = []

## Read header and create index of what columns the "place" field is in
header = spreadsheet.readline()
fields = header.split(",")
field_list = []
for i, item in enumerate(fields):
    lon_lat = []
    if item == "Place":
        field_list.append(i)

## Run through spreadsheet
for row in spreadsheet.readlines():
    values = row.split(",")
    track = {}
    track["Track Name"] = values[1]
    track_stops = []
    for index in field_list:
        if len(values[index]) > 0:
            track_stop = {}
            track_stop["Stop Name"] = values[index]
            lon_index = index + 2
            lat_index = index + 1
            lon_clean = float(values[lon_index].replace("*","").replace("L",""))
            lat_clean = float(values[lat_index].replace("*","").replace("L",""))
            track_stop["Lon Lat"] = [lon_clean,lat_clean]
            track_stops.append(track_stop)
    track["Track Stops"] = track_stops
    tracks.append(track)

spreadsheet.close()

## Output format

# tracks = [
#     track = {
#         "Track Name" : "Track A",
#         "Track Stops" : [{
#             "Stop Name" : "Stop A",
#             "Lon Lat" : ["-70","42"]
#         },{
#             "Stop Name" : "Stop B",
#             "Lon Lat" : ["-72","43"]
#         },{
#             "Stop Name" : "Stop C",
#             "Lon Lat" : ["-73","44"]
#         }...
#         ]
#     }
# ]

#### ArcGIS Portion

for track in tracks:
    arcpy.AddMessage(track["Track Name"])

    ## Create a new feature class for each track
    #track_feature = track["Track Name"].replace(" ","_").replace("-","_").replace("/","_").replace("(","_").replace(")","_").replace(".","_")
    arcpy.AddMessage(track_feature)
    # arcpy.CreateFeatureclass_management(output_location, track_feature, "POINT", "", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "", "0", "0", "0")
    # new_feature = output_location + "\\" + track_feature + ".shp"
    # arcpy.AddField_management(new_feature, "StopName", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
    #
    # cursor = arcpy.InsertCursor(new_feature)
    #
    # for stop in track["Track Stops"]:
    #     arcpy.AddMessage(stop["Stop Name"])
    #     arcpy.AddMessage(stop["Lon Lat"][0])
    #     arcpy.AddMessage(stop["Lon Lat"][1])
    #     feature = cursor.newRow()
    #     point = arcpy.Point()
    #     point.X = stop["Lon Lat"][0]
    #     point.Y = stop["Lon Lat"][1]
    #     point_geom = arcpy.PointGeometry(point, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision")
    #     feature.shape = point_geom
    #     feature.setValue("StopName", stop["Stop Name"])
    #     cursor.insertRow(feature)
    #
    # del cursor

arcpy.AddMessage("All done.")