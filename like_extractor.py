import json
import nltk
import os
import string
from dynamicVar import like_extractor_var

from collections import Counter

# open file
filenamearr = like_extractor_var()['sourcefile']
data = {}
for filename in filenamearr:

    with open(filename) as file:
        dict = json.load(file)

    data.update(dict)
    # print data
# print 'alldict', data
# print like_extractor_var()['targetfile']

def writeToFile(result):
    filename = like_extractor_var()['targetfile']
    print filename
    # harus ada pengecekan fileexist atau ga
    isExist = os.path.isfile(filename)
    if isExist == True :
        # kalo file exist
        file = open(filename, "a")
    else :
        # kalo file not exist
        file = open(filename, "w+")
    file.write(json.dumps(result))
    file.close()
    return True

def getLikeCategorySummary():
    resultToWrite = []
    x = []
    hits = 0
    numOfEnglishPostUser = 0

    for userid in data:
        if 'like' in data[userid]:
            # if len(data[userid]['like']) > 0:
            likevalue = data[userid]['like']
            arrayLike = [ i for i in likevalue ]
            x += arrayLike

            tempList = []
            arrayUniqueCat = {}
            count = 0

            for i, e in enumerate(x):
                if e not in tempList :
                    tempList.append(e)

            for item in tempList:
                count = 0
                for itemx in x:
                    if item == itemx :
                        count += 1
                arrayUniqueCat[item] = count
    resultToWrite = sorted(arrayUniqueCat.items(), key = lambda x:x[1], reverse=True)
    print resultToWrite
    writeToFile(resultToWrite)

def getUniqueLikeCategories():
    x = []
    for userid in data:
        if 'like' in data[userid]:
            likevalue = data[userid]['like']
            arrayLike = [ i for i in likevalue ]
            x += arrayLike
    return sorted(list(set(x)))

likeperuser = {}
matchvalue = []
alluserlike = []
column = getUniqueLikeCategories()

# coba di 1 user
userid = '10156164355355058'
likevalue = data[userid]['like']
"""
print likevalue
x = Counter(likevalue)

# [[x,l.count(x)] for x in set(l)]
y = [[z,likevalue.count(z)] for z in set(likevalue)]
print y
print column

value = 0
for cat in column:
    # print cat, likevalue
    if cat in likevalue:
        # print True
        value = likevalue.count(cat)
    else:
        # print False
        value = 0
    matchvalue.append(value)
likeperuser[userid] = matchvalue
print likeperuser
"""
# tambahi nama column
head = ['userid']
for cat in column:
    head.append(cat)
likeperuser['headrow'] = head
# value
for userid in data:
    if 'like' in data[userid]:
        likevalue = data[userid]['like']
        for cat in column:
            if cat in likevalue:
                value = likevalue.count(cat)
            else:
                value = 0
            matchvalue.append(value)
    # print matchvalue
    likeperuser[userid] = matchvalue
# print likeperuser
writeToFile(likeperuser)