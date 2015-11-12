# modules
import arcgisscripting, os, sys

# geoprocessing object
gp = arcgisscripting.create(9.3)

#loop through the directory
for root, dirs, files in os.walk("C:\\###\\###"):
    for name in files:
        gp.workspace = root #workspace
        date = name[10:18] #grabs date
        hypen = "-"
        hyphen_date = date[0:3] + hyphen+date[3:5] + hyphen + date[5:7] #add hyphensto date

        if name[name.rfind("."):len(name)] == ".shp": #get shapefiles
            print "adding field for this shapefile: " + name
            gp.addfield(name,"starting_date","DATE") # Add a datefield

    # update each row with the current date
            try:
                rows = gp.UpdateCursor(name)
                row = rows.Next()
            
                while row:
                    row.start_date = hyphendate
                    rows.UpdateRow(row)
                    row = rows.Next()

                del row, rows

            except:
                if not gp.GetMessages() == "":
                    gp.AddMessage(gp.GetMessages(2))