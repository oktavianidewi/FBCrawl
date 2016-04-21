import csv
import json

# base = 'constitutionalpatriot'
# base = 'foodgroups'
# base = 'monkeymajik'
# base = 'TEDtranslate'
base = 'traveladdiction'

filename = 'member'+base+'.json'
csvfilename = 'member'+base+'.csv'

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