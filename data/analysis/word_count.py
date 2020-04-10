import glob
import csv
import json
from collections import defaultdict


path = '../scripts/*.csv'

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

def parsePunctuation(line):
    line = line.lower()
    for x in line: 

        if x in punctuations: 
            line = line.replace(x, "") 

    return line

chars = defaultdict(lambda: defaultdict(int))
for fname in glob.glob(path):
    with open(fname, 'r') as script:
        reader = csv.DictReader(script)
        print(fname)
        for row in reader:
            line = parsePunctuation(row["Line"])
            line_list = line.split()

            for word in line_list:
                chars[row['Character']][word] += 1

with open("character_words.json", 'w') as fn:
    fn.write(json.dumps(chars))
fn.close()



    


