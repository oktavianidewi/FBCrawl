"""
import csv
with open('names.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
"""
import csv
outfile = file('test.csv','wb')
writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
writer.writerow(['hi','dude'])
writer.writerow(['hi2','dude2'])
outfile.close()