__author__ = 'Gauresh Pandit'
import sys,os
import re

names = {'amy', 'droid', 'shen-3gs'}
if(not os.path.exists('found_positives/')):
    os.makedirs('found_positives/')
for follow_folder in names:
    if(os.path.isfile("found_positives/" + follow_folder)):
        open("found_positives/" + follow_folder, 'w').close()
    #cheking for all files in the folders iteratively
    for file in os.listdir(follow_folder):
        dict = {}
        if os.path.getsize(follow_folder + "/" + file) <= 0 or '.' in file:
            continue
        rule = file.split("_")

        #this file doesnt have an appended rule
        if (len(rule) < 2):
            continue
        fileHandle = open(follow_folder + "/" + file, "r+")
        fileData = fileHandle.readlines()
        splits = []
        matchtab = []
        matches = []

        #Forming Tokens and splitting on different characters.
        for line in fileData:
            matchand = [s for s in line.split("&") if '=' in s or ':' in s]
            for ands in matchand:
                matchcomma = [s for s in ands.split(",") if '=' in s or ':' in s]
                for commas in matchcomma:
                    matchqmark = [s for s in commas.split("?") if '=' in s or ':' in s]
                    for qmark in matchqmark:
                        matchtab = [s for s in qmark.split("\t") if '=' in s or ':' in s]
                        matchtab = [s.replace(' ','') for s in [s.replace('"','') for s in matchtab]]
                        matchtab = [s for s in matchtab if len(s) < 50]
                        matches.extend(matchtab)

        print(file)
        kvpairs = {}
        allpairs = {}

        #For the found pairs splitting and finding positives.
        for match in matches:
            if('=' in match):
                kv = match.split('=')
                allpairs[kv[0]] = kv[1]
                if(rule[1] in kv[1]):
                    if(kv[0] in kvpairs.keys()):
                        kvpairs[kv[0]] = kvpairs[kv[0]] + 1
                    else:
                        kvpairs[kv[0]] = 1
            else:
                kv = match.split(':')
                allpairs[kv[0]] = kv[1]
                if(rule[1] in kv[1]):
                    if(kv[0] in kvpairs.keys()):
                        kvpairs[kv[0]] = kvpairs[kv[0]] + 1
                    else:
                        kvpairs[kv[0]] = 1
        strpairs = str(kvpairs)
        #print(strpairs)

        #Writing the found positives to file
        writeFile = open("found_positives/"+rule[0],"a+")
        writeFile.write(rule[1]+'\n')
        writeFile.write(strpairs+'\n')
        positives = []