import csv
import json
from dynamicVar import groupname, directory, presentFile, previousFile, stoppeduserid
import datetime

date = datetime.date.today().strftime('%m%d%Y')
def convertMember(base):
    filename = date+'_member'+base+'.json'
    csvfilename = date+'_member'+base+'.csv'

    outfile = file(csvfilename,'wb')
    writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Name", "UserID", "Administrator"])

    with open(filename) as data_file:
        json_data = json.load(data_file)
        for userinfo in json_data['data']:
            writer.writerow([
                userinfo['name'].encode('ascii', 'ignore').decode('ascii'),
                userinfo['id'].encode('ascii', 'ignore').decode('ascii'),
                userinfo['administrator']
            ])

    outfile.close()

def compareWithPreviousUser():
    previousUser = []
    presentUser = []
    with open(directory+'/'+presentFile, 'rb') as data_file:
        csv_data = csv.reader(data_file, delimiter=',')
        for row in csv_data:
            x = ', '.join(row)
            presentUser.append(x)
        presentUser.pop(0)
    # print len(presentUser)

    if previousFile != '':
        # print previousFile
        with open(directory+'/'+previousFile) as data_file:
            csv_data = csv.reader(data_file, delimiter=',')
            for row in csv_data:
                x = ', '.join(row)
                previousUser.append(x)
            previousUser.pop(0)

        # print len(previousUser)

        usernew = list(set(presentUser) - set(previousUser))
    else:
        usernew = list(set(presentUser))
    # print len(usernew)
    return usernew

def findIndex(userid):
    # 4744301940858
    print userid
    if userid == '0':
        stoppeduseridindex = 0
    else :
        newarr = compareWithPreviousUser()
        stoppeduseridindex = newarr.index(userid)
    return stoppeduseridindex

def convertPostInfo(base):
    filename = date+'_pi'+base+'.json'
    filtereduser = []
    csvfilename = date+'_piB'+base+'.csv'
    outfile = file(directory+'/'+csvfilename,'wb')
    writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    # writer.writerow(["Username", "UserID", "PostID", "updatedtime", "#reactions", "#comments"])
    writer.writerow(["UserID"])
    with open(directory+'/'+presentFile) as data_file:
        json_data = json.load(data_file)

        for postiteminfo in json_data['feed']['data']:
            # row yang ditulis: username, userid, postid, updated_time, #reaction (kalo ada), #comments
            print postiteminfo['from']
            if postiteminfo['from']['id'] not in filtereduser:
                filtereduser.append(postiteminfo['from']['id'])
            """
            if 'comments' in postiteminfo:
                no_comment = len(postiteminfo['comments']['data'])
            else:
                no_comment = 0
            if 'reactions' in postiteminfo:
                no_reaction = len(postiteminfo['reactions']['data'])
            else:
                no_reaction = 0
            """
    for x in filtereduser:
        writer.writerow([x])
    outfile.close()

# convertPostInfo(groupname)
# print compareWithPreviousUser()
# print findIndex(stoppeduserid)