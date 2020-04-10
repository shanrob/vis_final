import glob
import csv
import json
from collections import defaultdict
import collections
import re

path = '../scripts/*.csv'

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''



def parsePunctuation(line):
    for x in line: 

        if x in punctuations: 
            line = line.replace(x, "") 

    return line


## count of words each character says
num_words = defaultdict(int)
chars_words = defaultdict(lambda: defaultdict(int))
char_names = set()
for fname in glob.glob(path):
    with open(fname, 'r') as script:
        reader = csv.DictReader(script)
        print(fname)
        for row in reader:
            line = parsePunctuation(row["Line"])
            line_list = line.split()
            num_words[row['Character']] += len(line_list)
            char_names.add(row['Character'])
            for word in line_list:
                chars_words[row['Character']][word] += 1

with open("character_words.json", 'w') as fn:
    fn.write(json.dumps(chars_words))
fn.close()




# with open('character_names.csv', 'w', newline='') as csvfile:
#     fieldnames = ["Name", "Gender"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
#     writer.writeheader()
    
#     for item in char_names:
#         row = collections.OrderedDict()
#         row["Name"] = item
#         row["Gender"] = "female"
#         writer.writerow(row)
# csvfile.close()


done = sorted([(k, v) for k, v in num_words.items()], key=lambda x: x[1], reverse = True)
with open('character_word_count.csv', 'w', newline='') as csvfile:
    fieldnames = ["Name", "Num_words_said"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for x, y in done:
        row = collections.OrderedDict()
        row["Name"] = x
        row["Num_words_said"] = y
        writer.writerow(row)
        


