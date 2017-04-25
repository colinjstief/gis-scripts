__author__ = 'cstief'

import arcpy,os

InFolder = r"C:\Users\ChesConserv1\Desktop\Colin_GIS\Randolph\Randolph6"
Dest= r"C:\Users\ChesConserv1\Desktop\Colin_GIS\Randolph\Randolph6"

arcpy.env.workspace=InFolder
#The raster datasets in the input workspace
in_raster_datasets = arcpy.ListRasters()
print(in_raster_datasets)

Location = os.path.dirname(Dest)
Name = os.path.basename(Dest) + "_footprint.shp"
Template = r"\\Ccsvr01\d\GIS\Conservation_Innovation\Classification_Resources\ESRI_Leaf_Off_Tools\WVSegmentationMaterials\projection.shp"

Footprint = arcpy.CreateFeatureclass_management(Location, Name, "POLYGON","","","", Template)
arcpy.AddField_management(Footprint,"RasterName", "String","","",250)
arcpy.AddField_management(Footprint,"RasterPath", "String","","",250)

cursor = arcpy.InsertCursor(Footprint)
point = arcpy.Point()
array = arcpy.Array()
corners = ["lowerLeft", "lowerRight", "upperRight", "upperLeft"]
for Ras in in_raster_datasets:
    feat = cursor.newRow()
    r = arcpy.Raster(Ras)
    for corner in corners:
        point.X = getattr(r.extent, "%s" % corner).X
        point.Y = getattr(r.extent, "%s" % corner).Y
        array.add(point)
    array.add(array.getObject(0))
    polygon = arcpy.Polygon(array)
    feat.shape = polygon
    feat.setValue("RasterName", Ras)
    feat.setValue("RasterPath", InFolder + "\\" + Ras)
    cursor.insertRow(feat)
    array.removeAll()
del feat
del cursor