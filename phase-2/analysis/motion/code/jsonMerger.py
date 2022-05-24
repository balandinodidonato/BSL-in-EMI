# This script merges all json file from a folder into a JSON file named as the name of the folder path

import glob, json
import sys

path = str(sys.argv[1])
data = []

for f in glob.glob(path+"/*.json"):

    with open(f,) as infile:
      
        data.append(json.load(infile))
         
with open(path+".json",'w') as outfile:

  json.dump(data, outfile)