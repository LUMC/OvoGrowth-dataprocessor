import sys
from os import path
arg = sys.argv


def validate_input(files_dataset, required_files):
    if len(files_dataset) < 1:
        print("No valid dataset files detected")
    for file_set in files_dataset:
        for rfile in required_files:
            if (not path.exists(file_set+"/"+rfile)):
                print(file_set+"/"+rfile+ " are required but missing")
    return True

if (validate_input(arg[0], arg[1])):
    open(arg[2], 'w').write("correct")