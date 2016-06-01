import json
from dynamicVar import user_distribution_var
from like_extractor import getUserLike

# open file
def open_multiple_english(filenamearr):
    data = []
    for filename in filenamearr:
        with open(filename) as file:
            dict = json.load(file)
            print len(dict)
            for i in dict :
                data.append(i)
    return data

def open_multiple_all(filenamearr):
    data = {}
    for filename in filenamearr:
        with open(filename) as file:
            dict = json.load(file)
        data.update(dict)
    return data


english_sourcefile = user_distribution_var()['english_sourcefile']
# all_sourcefile = user_distribution_var()['all_sourcefile']

rows = open_multiple_all(english_sourcefile)
userlike = getUserLike()
# print rows
err = 0
tlempty = 0

import csv
userarr = []
directory = 'extracted'
csvfilename = '1.csv'
outfile = file(directory+'/'+csvfilename, 'wb')
writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
# urutannya : userid, numposts, startdatepost, enddatepost, likerow

columnlike = userlike['headrow'][1:]
head = ['userid', 'numposts', 'startdatepost', 'enddatepost']
for x in columnlike:
    head.append(x)

writer.writerow(head)

for i in rows:
    userposts = rows[i]
    numpost = len(userposts['timeline'])
    # print i
    # print numpost

    try:
        startdatepost = min(userposts['timeline'])[6]
        enddatepost = max(userposts['timeline'])[6]
    except Exception, e:
        startdatepost = 'None'
        enddatepost = 'None'
        tlempty += 1

    # print startdatepost
    # print enddatepost

    try:
        userlikelist = userlike[i]
    except Exception, e:
        err += 1
        userlikelist = 'None'

    userarr.append([i, startdatepost, enddatepost, userlikelist])
    for y in userlikelist:
        userarr.append(y)

    writer.writerow(userarr)
outfile.close()

print 'like kosong : ', err
print 'tl kosong : ', tlempty
print userarr

# proses writing data


