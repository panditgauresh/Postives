__author__ = 'Gauresh Pandit'
import sys,os
import re
import ast

names = {'amy', 'droid', 'shen-3gs'}

#Method to print the top three count valued keys in the dictionary into the file.
def printTop3Dict(dict,writeFalse):
        first = second = third = 0
        firstval = ''
        secondval = ''
        thirdval = ''
        for key,value in dict.items():
            if(value >= first):
                third = second
                second = first
                first = value
                thirdval = secondval
                secondval = firstval
                firstval = key
            elif(value>=second):
                third = second
                second = value
                thirdval = secondval
                secondval = key
            elif (value>=third):
                third = value
                thirdval = key

        if(firstval != ''):
            writeFalse.write(firstval + ":" + str(first))
        if(secondval != ''):
            writeFalse.write(', '+secondval + ":" + str(second))
        if(thirdval != ''):
            writeFalse.write(', '+thirdval + ":" + str(third))
if(not os.path.exists('false_positives1')):
    os.makedirs('false_positives1')

#For the name in the list find the false positives iteratively
for name in names:
    if(os.path.isfile("false_positives1/" + name)):
        open("false_positives1/" + name, 'w').close()
    else:
        open("false_positives1/" + name, 'w+').close()
    matchtab = []
    matches = []
    for file in os.listdir('positive'):
        if name not in file:
            continue

        fileHandle = open("positive/" + file, "r+")
        fileData = fileHandle.readlines()

        #
        for line in fileData:
            matchand = [s for s in line.split("&") if '=' in s or ':' in s]
            for ands in matchand:
                matchcomma = [s for s in ands.split(",") if '=' in s or ':' in s]
                for commas in matchcomma:
                    matchqmark = [s for s in commas.split("?") if '=' in s or ':' in s]
                    for qmark in matchqmark:

                        matchtab = [s for s in qmark.split("\t") if '=' in s or ':' in s]
                        matchtab = [s.replace(' ','') for s in [s.replace('"','') for s in matchtab]]

                        for tabs in matchtab:
                            matchsemilcol = [s for s in tabs.split(';') if '=' in s or ':' in s]
                            matchsemilcol = [s for s in matchsemilcol if len(s) < 100]
                            matches.extend(matchsemilcol)
    negatives = {}
    #print(matches)
    positiveList = []
    if(os.path.isfile('found_positives/'+name)):
        fileHandle = open("found_positives/" + name, "r+")
        fileData = fileHandle.readlines()
        for i in range(0,len(fileData),2):
            positiveList.append(fileData[i].rstrip())
    #print(positiveList)

    if(os.path.isfile('found_positives/'+name)):
        fileHandle = open("found_positives/" + name, "r+")
        fileData = fileHandle.readlines()
        for i in range(0,len(fileData),2):
            #print("1:"+fileData[i])
            #print("2:"+fileData[i+1])

            for key in list(ast.literal_eval(fileData[i+1].rstrip()).keys()):
                negatives = {}
                negativecount = {}
                for match in matches:
                    if('=' in match):
                        kv = match.split('=')
                    else:
                        kv = match.split(':')
                    if(kv[0] == key):
                        if(kv[1] != fileData[i].rstrip() and kv[1] not in positiveList):
                            if(kv[0] in negatives.keys() and kv[1] != ''):
                                negatives[kv[0]] = negatives[kv[0]] + 1
                            else:
                                negatives[kv[0]] = 1
                            if(not kv[1] in negativecount.keys()):
                                negativecount[kv[1]] = 1
                            elif(kv[1] != ''):
                                negativecount[kv[1]] = negativecount[kv[1]] + 1
                print(key)
                strneg = str(negatives)
                strnegs = str(negativecount)
                print(strneg)
                if(negatives):
                    writeFalse = open('false_positives1/' + name,'a+')
                    writeFalse.write(key+'\n')
                    writeFalse.write(strneg+"\n")
                    printTop3Dict(negativecount,writeFalse)
                    writeFalse.write('\n')
                print(negativecount)