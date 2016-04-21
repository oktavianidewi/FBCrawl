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
3.	TED Translate (Education, closed group) https://www.facebook.com/groups/ITranslateTEDTalks/
4.	Travel Addiction (Hobby, public group) https://www.facebook.com/groups/2363953408
5.	Monkey Majik (Music, closed group) https://www.facebook.com/groups/2232297350/

to find id: https://lookup-id.com

curl -i -X GET
"https://graph.facebook.com/v2.5/226871267323666/members?limit=4351&access_token=CAACEdEose0cBALPcx29mkaTS4yNSAqWeyXoM5bBYJENZA63W7xhcaI7dyOMiD0vlbbWs1TS0oDMkRMhx63SGZBENI0OgyT6ttISUZCIZCc2sqpfVsjGCO03Hgg1DZAcqBA2b59WpYeelxHux3Cj0BjN3oSJoKd6wMPqGEm3Dq4NQYUZAP1qmgJCLCPu4P0XBCTZCRmErE9vbz8pW3Aqfy82"
"""

# python 2.7
from urllib import urlopen
import json

oauth = "CAACEdEose0cBADcNP15dZCo4PZBPQj0nRAIvNtIZBRxUBq6XrLW4APTaRBOfvbKliEBwIjHGkhkhYDM94X35CwZCojtXJGvAl938KF4cG2SioZC2VpOUNtba2ytwWFibhnlcWzp3kQRYHo1y1GXfFBkHszwHKP1u4o33EZBjgfZBIul3a47jQLdDVw8RbKscWh5Q1irFELEprexjQoDkGsN"
limit = "500"

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
    jsonfile = type+groupname+fileformat

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
    print feedurl
    quit()
    writeprocess = writeToJsonFile(feedurl, jsonfile)
    return writeprocess

def getGroupInfo():
    pass

def writeToJsonFile(url, jsonfile):
    result = urlopen(url)
    read = result.read()
    file = open(jsonfile, "wb")
    file.write(read)
    file.close()
    return True

# to get group member
# getGroupMember('constitutionalpatriot', limit, oauth)
# getGroupMember('foodgroups', limit, oauth)
# getGroupMember('traveladdiction', limit, oauth)
# getGroupMember('monkeymajik', limit, oauth)
# getGroupMember('TEDtranslate', limit, oauth)

# to get group feed
# getGroupFeed('constitutionalpatriot', limit, oauth)
# getGroupFeed('foodgroups', limit, oauth)
# getGroupFeed('traveladdiction', limit, oauth)
getGroupFeed('monkeymajik', limit, oauth)
# getGroupFeed('TEDtranslate', limit, oauth)

# file = open("foodgroups.json", "wb")
# file = open("recipeshare.json", "wb")
# file = open("constitutionalpatriots.json", "wb")
# file = open("feedfoodgroups.json", "wb")
"""
file = open("feedconstitutionalpatriot.json", "wb")
file.write(read)
file.close()
"""