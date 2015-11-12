__author__ = 'duncanrager'

import os, sys, fileinput, shutil

out_directory = "/Users/duncanrager/Desktop/TRANSFER/Original/dynamic-dependant-dropdown/dynamic_dropdown/classic/js/"
in_directory = out_directory + "states"
final_script = open(out_directory + "states.js", "w")

# Walk through directory
for root, dirs, files in os.walk(in_directory):

    # For every file in all of the files of the directory, do something
    for file in files:

        infile = open(os.path.join(root, file))

        # Construct the state abbreviation from filename and capitalize it with parentheses
        short_name = file[:2]
        short_tall_name = short_name.upper()
        final_name = " (" + short_tall_name + ")"
        new_value = "County" + final_name

        # Construct new function name
        function_name = short_name + "_populate(select_box)"

        # Construct the full file name so that we can open it
        #fullpath = os.path.join(root, file)

        for line in infile:
            line = line.replace("populate(form)", function_name).replace("form.options","select_box.prop('options')").replace("County", new_value)
            final_script.write(line)

        infile.close()

final_script.close()