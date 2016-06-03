import json
import csv
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

from operator import itemgetter

def getTopLimit():
    # english_sourcefile = user_distribution_var()['english_sourcefile']

    english_sourcefile = [
        'extracted/english_TEDtranslate.json', 'extracted/english_traveladdiction.json', 'extracted/english_constitutionalpatriot.json',
        'extracted/english_Hiking With Dogs.json', 'extracted/english_Like For Like Promote Your Business.json', 'extracted/english_Jazzmasters&Jaguars.json'
    ]
    rows = open_multiple_all(english_sourcefile)
    userlike = getUserLike()

    jumlaharr= []
    columnlike = userlike['headrow'][1:]
    # print columnlike
    # print userlike
    # rows = ['10152908300611754', '569990716438198']
    # ok = [3, 4]

    for i, v in enumerate(columnlike):
        jumlah = 0
        for userid in rows:
            try:
                k = userlike[userid][i]
            except Exception, e:
                k = 0
            jumlah = jumlah + k
        jumlaharr.append([v, jumlah])
    print 'Top-30 most liked subcategories from : ', english_sourcefile
    sortedlist = sorted(jumlaharr, key=itemgetter(1), reverse=True)
    # print sortedlist
    top30 = []
    for index in range(0, 50):
        print sortedlist[index]
        # top30.append(sortedlist[index])
    # return sortedlist
    return top30

getTopLimit()
quit()

def userdist_all(topLimit, *args):
    english_sourcefile = user_distribution_var()['english_sourcefile']
    # all_sourcefile = user_distribution_var()['all_sourcefile']

    rows = open_multiple_all(english_sourcefile)
    userlike = getUserLike()

    # print rows
    err = 0
    tlempty = 0

    userarr = []
    directory = 'extracted'
    # csvfilename = user_distribution_var()['targetfile']
    csvfilename = 'english_all_110.csv'
    outfile = file(directory+'/'+csvfilename, 'wb')
    writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    # urutannya : userid, group, numposts, recentdatepost, olddatepost, likerow

    columnlike = userlike['headrow'][1:]
    # print len(columnlike)
    # print columnlike
    columnlikelimit = []
    columnlikeindex = []
    if topLimit == 'betul':
        topLimitArr = getTopLimit()
        for sub in topLimitArr:
            # print sub[0]
            # print columnlike.index(sub[0])
            columnlikeindex.append(columnlike.index(sub[0]))
            columnlikelimit.append(sub[0])

    # print columnlikelimit

    head = ['userid', 'group', 'numposts', 'olddatepost', 'recentdatepost']
    # for x in columnlike:
    for x in columnlikelimit:
        head.append(x.encode('ascii', 'ignore').decode('ascii'))
    writer.writerow(head)
    for userid in rows:
        userposts = rows[userid]
        try:
            group = userposts['group']
        except Exception, e:
            group = 'Foodgroup'
        try:
            numpost = len(userposts['timeline'])
        except Exception, e:
            numpost = '0'
        # print i
        # print numpost

        try:
            recentdatepost = min(userposts['timeline'])[6]
            olddatepost = max(userposts['timeline'])[6]
        except Exception, e:
            recentdatepost = None
            olddatepost = None
            tlempty += 1

        # print recentdatepost
        # print olddatepost
        try:
            userlikelist = userlike[userid]
        except Exception, e:
            err += 1
            # userlikelist = ['0' for x in len(columnlike)]
            # userlikelist = len(columnlike) * ['0']
            userlikelist = len(columnlikelimit) * ['0']
            # userlikelist = 'None'

        userarr = [str(userid), group, numpost, olddatepost, recentdatepost]

        # ukuran userlikelist kan berbeda2
        # print userlikelist

        for ilimit in columnlikeindex:
            # print ilimit
            try:
                y = userlikelist[ilimit]
            except Exception, e:
                y = 0
                # print 'kosong'
            # userarr.append(userlikelist[ilimit])
            userarr.append(y)
        """
        for y in userlikelist:
            if y != 'None':
                userarr.append(y)
            else:
                userarr.append(None)
        """
        # print userarr
        writer.writerow(userarr)
    outfile.close()

    print 'like kosong : ', err
    print 'tl kosong : ', tlempty
    # print userarr


topLimit = 'betul'
userdist_all(topLimit)
# proses writing data


