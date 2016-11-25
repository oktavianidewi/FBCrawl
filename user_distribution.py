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
    if type(filenamearr) is list:
        # print 'list'
        data = {}
        for filename in filenamearr:
            with open(filename) as file:
                dict = json.load(file)
            data.update(dict)
    else:
        # print 'bukan list'
        with open(filenamearr) as file:
            data = json.load(file)
    return data

from operator import itemgetter
english_sourcefile = user_distribution_var()['english_sourcefile']

def getTopLimit(maxlimit, english_sourcefile):
    # masing2 file
    # , 'extracted/english_traveladdiction.json', 'extracted/english_constitutionalpatriot.json','extracted/english_Hiking With Dogs.json', 'extracted/english_Like For Like Promote Your Business.json', 'extracted/english_Jazzmasters&Jaguars.json'
    '''
    english_sourcefile = [
        'extracted/english_TEDtranslate.json'
    ]

    # semua file
    english_sourcefile = [
        'extracted/english_TEDtranslate.json', 'extracted/english_traveladdiction.json', 'extracted/english_constitutionalpatriot.json',
        'extracted/english_Hiking With Dogs.json', 'extracted/english_Like For Like Promote Your Business.json', 'extracted/english_Jazzmasters&Jaguars.json'
    ]
    '''
    rows = open_multiple_all(english_sourcefile)
    userlike = getUserLike(english_sourcefile)
    print 'english : ', english_sourcefile
    # print userlike

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
    # print 'Top-30 most liked subcategories from : ', english_sourcefile
    sortedlist = sorted(jumlaharr, key=itemgetter(1), reverse=True)
    if maxlimit > 0:
        return sortedlist[:maxlimit]
    else:
        return sortedlist

def irisanLikedGroup(english):
    # print english_sourcefile
    topLimitArrAll = []
    for x in english:
        print x
        # topLimitArr = getTopLimit(10, x)
        topLimitArrAll.append([ z[0] for z in getTopLimit(10, x) ])
    irisan = []
    for topLimitArr in topLimitArrAll:
        for single in topLimitArr :
            if single not in irisan:
                irisan.append(single)
    # print len(irisan)
    return irisan

# print irisanLikedGroup(english_sourcefile)
"""
print len(getTopLimit(0))
for x in getTopLimit(0):
    print x
quit()
"""

def csvCategoryNLikes():
    directory = 'extracted'
    csvfilename = user_distribution_var()['targetfilecategoryonly']
    outfile = file(directory+'/'+csvfilename, 'wb')
    writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    data = getTopLimit(0, english_sourcefile)
    head = ['category', 'likecount']
    writer.writerow(head)
    # for x in columnlike:
    for x in data:
        # print x[0].replace(',', '-')
        x[0] = x[0].replace(',', '-')
        print x
        # untuk mengubah ',' pada kolom dengan '-'
        # head.append(x.replace(',','-').encode('ascii', 'ignore').decode('ascii'))
        writer.writerow(x)
    outfile.close()
# print getTopLimit(0)

# csvCategoryNLikes()


def userdist_all(topLimit, *args):
    # all_sourcefile = user_distribution_var()['all_sourcefile']
    rows = open_multiple_all(english_sourcefile)

    # merge dari semua file
    userlike = getUserLike(english_sourcefile)

    # print rows
    err = 0
    tlempty = 0

    userarr = []
    directory = 'extracted'
    csvfilename = user_distribution_var()['targetfile']
    # csvfilename = 'english_all_110.csv'
    outfile = file(directory+'/'+csvfilename, 'wb')
    writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    # urutannya : userid, group, numposts, recentdatepost, olddatepost, likerow

    #
    # columnlike = userlike['headrow'][1:]
    columnlike = irisanLikedGroup(english_sourcefile)
    # print len(columnlike)
    # print columnlike
    columnlikelimit = []
    columnlikeindex = []
    if topLimit == 'betul':
        topLimitArr = getTopLimit(0, english_sourcefile)
        topLimitArrNoValue = sorted([ sub[0] for sub in topLimitArr ])

        for sub in columnlike:
            columnlikeindex.append(topLimitArrNoValue.index(sub))
            columnlikelimit.append(sub)
            # jumlahnya salah
        """
        # untuk yang semua data
        for sub in topLimitArrNoValue:
            columnlikeindex.append(columnlike.index(sub))
            columnlikelimit.append(sub[0])
        """

    # untuk testing
    print columnlikeindex
    print columnlikelimit
    """
    print 'limit arr' , sorted(topLimitArrNoValue)
    for x in userlike:
        print x
    quit()
    """


    # print columnlikelimit

    head = ['userid', 'group', 'numposts', 'olddatepost', 'recentdatepost']
    # for x in columnlike:
    for x in columnlikelimit:
        # untuk mengubah ',' pada kolom dengan '-'
        head.append(x.replace(',','-').encode('ascii', 'ignore').decode('ascii'))
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
            print ilimit
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

    # print 'like kosong : ', err
    # print 'tl kosong : ', tlempty
    # print userarr


topLimit = 'betul'
userdist_all(topLimit)
# proses writing data


