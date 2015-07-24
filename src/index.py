from os import listdir
from sys import argv
import json
import re

JSON_EXT = re.compile('.json$')

files = filter(lambda x: not x.startswith('index.'), listdir(argv[1]))
files = map(lambda x: JSON_EXT.sub('', x), files)
print "var domains = {};".format(json.dumps(files))

