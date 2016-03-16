from urllib.request import urlopen
import json

fbgroupid = "227049364011004"
limit = "6284"
oauth = "CAACEdEose0cBALPcx29mkaTS4yNSAqWeyXoM5bBYJENZA63W7xhcaI7dyOMiD0vlbbWs1TS0oDMkRMhx63SGZBENI0OgyT6ttISUZCIZCc2sqpfVsjGCO03Hgg1DZAcqBA2b59WpYeelxHux3Cj0BjN3oSJoKd6wMPqGEm3Dq4NQYUZAP1qmgJCLCPu4P0XBCTZCRmErE9vbz8pW3Aqfy82"

url = "https://graph.facebook.com/v2.5/%s/members?limit=%s&access_token=%s" %(fbgroupid, limit, oauth)
result = urlopen(url)
read = result.read()

# print(read)
# kenapa wb? maybe wb untuk write binary

# file = open("foodgroups.json", "wb")
file = open("recipeshare.json", "wb")
file.write(read)
file.close()

"""
Recipe Share
https://www.facebook.com/groups/227049364011004/?ref=br_rs


Food Groups
https://www.facebook.com/groups/226871267323666/?ref=br_rs

curl -i -X GET
"https://graph.facebook.com/v2.5/226871267323666/members?limit=4351&access_token=CAACEdEose0cBALPcx29mkaTS4yNSAqWeyXoM5bBYJENZA63W7xhcaI7dyOMiD0vlbbWs1TS0oDMkRMhx63SGZBENI0OgyT6ttISUZCIZCc2sqpfVsjGCO03Hgg1DZAcqBA2b59WpYeelxHux3Cj0BjN3oSJoKd6wMPqGEm3Dq4NQYUZAP1qmgJCLCPu4P0XBCTZCRmErE9vbz8pW3Aqfy82"

"""

"""
oauth_access_token = 'CAACEdEose0cBAGbiS8qO7oZBf8Lk25SHmbvh8yGZArAmCymB19HaZAH7TfhKka0VWZCfVEVvv1knXcUVBCA7Oddd0kDEf4leKzMCOhxdgN0cXZAGSF5Yag2RkgEjCZCV6Eib2PIlrtjdKo953ecUEyCznNOpMib0yvIsFhkyWF7J2XiUHesr7ruL1EERNeSWfoJjE41ixYXzOAPzGde5ZAU'
graph = facebook.GraphAPI(oauth_access_token)
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")

print(friends)
"""