import json
from dynamicVar import user_distribution_var

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
all_sourcefile = user_distribution_var()['all_sourcefile']

rows = open_multiple_english(english_sourcefile)
# print len(open_multiple_english(english_sourcefile))

all_rows = open_multiple_all(all_sourcefile)
# print len(open_multiple_all(all_sourcefile))

# englishonly = []
englishonly = {}
for row in rows:
    if row['englishpost'] > 20:
        # englishonly.append(all_rows[row['userid']])
        englishonly[row['userid']] = all_rows[row['userid']]
    # row['userid']

print 'jumlah user english ', len(englishonly)

# untuk mengambil no of post
for english_userid in englishonly:
    englishrow = englishonly[english_userid]
    timelines = englishrow['timeline']
    # print min(timelines) print max(timelines)
    print english_userid, 'no of post : ' , len(timelines)
    print 'tanggal awal :', timelines[0][6]
    print 'tanggal akhir :',timelines[len(timelines)-1][6]

