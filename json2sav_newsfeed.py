from savReaderWriter import SavWriter
import json, csv

dict_header_mlevel = {}
dict_header_type = {}
arr_header = []
csvfile = open('header_type_json_timeline.csv', 'rb')
csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
for row in csvreader:
    arr_header.append(row[0])
    dict_header_type[row[0]] = int(row[2])
    dict_header_mlevel[row[0]] = row[3]

# baca file json
json_file = "extracted/english_TEDtranslate_new.json"
json_data = json.load(open(json_file))
# print json_data['']['timeline']
# ok = ['957808000977133']

# save to json
# records = [[b'Test1', 1, 1], [b'Test212313', 2, 1]]
# varTypes = {'var1': 5, 'v2': 0, 'v3': 0}
savFileName = 'extracted/english_TEDtranslate_new.sav'
varNames = arr_header
varTypes = dict_header_type
mlevel_type = dict_header_mlevel

p = 0
with SavWriter(savFileName, varNames, varTypes, ioUtf8=1) as writer:
# with SavWriter(savFileName, varNames) as writer:
    for user in json_data:
        print user
        # print len(json_data[user]['timeline'][1])
        if user != '.DS_Store':
            for post in json_data[user]['timeline']:
                # print 'a', len(post)
                post = [user]+post
                # print post
                try:
                    if len(post) < len(varNames):
                        additional_value = [''] * ( len(varNames) - len(post) )
                        post = post + additional_value
                    elif len(post) > len(varNames):
                        post = post[0:len(varNames)]
                    writer.writerow(post)
                except:
                    pass
        """
        for post in json_data[user]['timeline']:
            writer.writerow(post)
        """
# pilih bagian timeline

        # tuliskan di sav


