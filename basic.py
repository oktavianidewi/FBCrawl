"""
try:
    # for python 3.5
    from urllib.request import Request, urlopen, URLError
except ImportError:
    # for python 2.7
    from urllib2 import Request,urlopen, URLError

Groups:
1.	Constitutional Patriots (Politic, public group): https://www.facebook.com/groups/394462630661212/
2.	Food Groups (Food, public group) https://www.facebook.com/groups/226871267323666
3.	TED Translate (Education, closed group) https://www.facebook.com/groups/43410681471
4.	Travel Addiction (Hobby, public group) https://www.facebook.com/groups/2363953408
5.	Monkey Majik (Music, closed group) https://www.facebook.com/groups/2232297350/
-----
6.  Learn Japanese with Tae Kim https://www.facebook.com/groups/214419481973565
to find id: https://lookup-id.com

curl -i -X GET
"https://graph.facebook.com/v2.5/226871267323666/members?limit=4351&access_token=CAACEdEose0cBALPcx29mkaTS4yNSAqWeyXoM5bBYJENZA63W7xhcaI7dyOMiD0vlbbWs1TS0oDMkRMhx63SGZBENI0OgyT6ttISUZCIZCc2sqpfVsjGCO03Hgg1DZAcqBA2b59WpYeelxHux3Cj0BjN3oSJoKd6wMPqGEm3Dq4NQYUZAP1qmgJCLCPu4P0XBCTZCRmErE9vbz8pW3Aqfy82"

API
1. to get userInfo who like a feed : 2363953408?fields=feed{likes}
2. to get userInfo who react a feed (bisa like, sedih, etc) : fields=feed.limit(20){reactions,comments,from} -> API v2.6
query to get posts based on user is restricted. But, it is possible to get all posts information (how many like, who post, comment, etc) on group

"""

# python 2.7
from urllib import urlopen
import json
import datetime
from dynamicVar import oauth, limit, groupname, directory
import os

date = datetime.date.today().strftime('%m%d%Y')

def groupInfo(groupname, type):
    if groupname == 'constitutionalpatriot':
        fbgroupid = "394462630661212"
    if groupname == 'foodgroups':
        fbgroupid = "226871267323666"
    if groupname == 'TEDtranslate':
        fbgroupid = "43410681471"
        fbgroupname = "ITranslateTEDTalks"
    if groupname == 'traveladdiction':
        fbgroupid = "2363953408"
    if groupname == 'monkeymajik':
        fbgroupid = "2232297350"

    fileformat = '.json'
    jsonfile = date+'_'+type+groupname+fileformat

    return fbgroupid, jsonfile

def getGroupMember(groupname, limit, oauth):
    type = 'member'
    groupinforesult = groupInfo(groupname, type)
    fbgroupid = groupinforesult[0]
    jsonfile = groupinforesult[1]

    memberurl = "https://graph.facebook.com/v2.5/%s/members?limit=%s&access_token=%s" %(fbgroupid, limit, oauth)
    writeprocess = writeToJsonFile(memberurl, jsonfile)
    return writeprocess

def getGroupFeed(groupname, limit, oauth):
    type = 'feed'
    groupinforesult = groupInfo(groupname, type)
    fbgroupid = groupinforesult[0]
    jsonfile = groupinforesult[1]
    feedurl = "https://graph.facebook.com/v2.5/%s?fields=feed.limit(%s)&access_token=%s" %(fbgroupid, limit, oauth)

    writeprocess = writeToJsonFile(feedurl, jsonfile)
    return writeprocess

def getPostsInfo(groupname,limit,oauth):
    type = 'pi'
    groupinforesult = groupInfo(groupname, type)
    fbgroupid = groupinforesult[0]
    jsonfile = groupinforesult[1]
    # limit parameter override since parameter
    feedurl = "https://graph.facebook.com/v2.6/%s?fields=feed.limit(%s){updated_time,from,reactions,comments}&access_token=%s" %(fbgroupid,limit,oauth)
    print feedurl
    writeprocess = writeToJsonFile(feedurl, jsonfile)
    return writeprocess

def getGroupInfo():
    pass

def directoryexist(dir):
    # create folder
    directory = dir
    if not os.path.exists(directory):
        os.makedirs(directory)
    directoryIsExist = True
    return directoryIsExist

def writeToJsonFile(url, jsonfile):
    checking = directoryexist(directory)
    result = urlopen(url)
    read = result.read()
    file = open(directory+'/'+jsonfile, "wb")
    file.write(read)
    file.close()
    return True

# to get group feed
# getGroupFeed(groupname, limit, oauth)

# to get userid who post
getPostsInfo(groupname, limit, oauth)
