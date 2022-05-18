import glob, json
import sys

path = str(sys.argv[1])
# filename = str(sys.argv[1])
data = []

for f in glob.glob(path+"/*.json"):

    with open(f,) as infile:
      
        data.append(json.load(infile))
         
with open(path+".json",'w') as outfile:

  json.dump(data, outfile)