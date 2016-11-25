import savReaderWriter as sav
import json
import os

def readSav():
    sourcefile = 'dataset/271_all_post.sav'
    targetfile = '271_user.json'

    with sav.SavReader(sourcefile) as reader:
        records = reader.all()

    userarr = []
    print len(records)
    for i in records:
        userarr.append(i[2])
    unique = list(set(userarr))

    with open('dataset/'+targetfile, 'w') as file:
        file.write( json.dumps(unique) )
        file.close()

def readJson():
    readUser = []
    with open('dataset/271_user.json', 'r') as data_file:
        urls = json.load(data_file)
    for i in urls:
        readUser.append(i.split('/')[3])
    return readUser

def checkCrawledUser():
    crawledUser = []
    foldername = 'dataset/20160520_271_user'
    # for root, dirs, files in os.walk(directoryGroup):
    for root in os.walk(foldername):
        arr = root[0].split('\\')
        if len(arr) > 1:
            crawledUser.append(arr[1])
    return crawledUser

def countExtracted():
    hitValid = 0
    validUser = []
    with open('extracted/20160520_271_user.json', 'r') as data_file:
        data = json.load(data_file)
    for userid in data:
        if 'timeline' in data[userid]:
            hitValid += 1
            validUser.append(userid)
    return validUser

"""
a = readJson()
b = readSavGroupUser()
print a
print b
selisih = list(set(a) - set(b))
print "jumlah selisih : ", len(selisih)
print "selisih : ", selisih

# untuk mengetahui selisih antara list of user dengan crawled user di folder
x = readJson()
y = checkCrawledUser()
selisih = list(set(x) - set(y))

for i in selisih:
    print i
    print x.index(i)

x = readJson()
a = countExtracted()
print sorted(x)
print sorted(countExtracted())
selisihNotExtracted = list(set(x) - set(a))
print len(selisihNotExtracted)
for i in selisihNotExtracted:
    print i
"""