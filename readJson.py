import re
import json
import nltk
from textblob import TextBlob, Blobber
from textblob.taggers import NLTKTagger
from textblob.sentiments import NaiveBayesAnalyzer
import csv

def getData(nama_file):
    token = []
    with open(nama_file) as data_file:
        json_data = json.load(data_file)
        for post in json_data['feed']['data']:
            for index, metadata in enumerate(post):
                if metadata == 'message':
                    x = post['message'].encode('ascii', 'ignore').decode('ascii')
                    token.append(x)
    return token

def removeURL(message):
    # remove URLs
    # ([^0-9A-Za-z \t])| -> to remove punctuation !.,
    messagenourl = ' '.join(re.sub("(\w+:\/\/\S+)"," ", message).split())
    return messagenourl

def subj_polar(message):
    blob = TextBlob(message)
    polarity  = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    # result = 'SubjPolar(subjectivity=%s, polarity=%s)' %(subjectivity, polarity)
    # return result
    return subjectivity, polarity

def pos_tagger(message):
    nltk_tagger = NLTKTagger()
    pos_tagged = TextBlob(message, pos_tagger=nltk_tagger)
    return pos_tagged.pos_tags

def advancedsentiment(message):
    # message = unicode(message, 'utf8')
    sent = TextBlob(message, analyzer=NaiveBayesAnalyzer())
    classification = sent.sentiment.classification
    posvalue = sent.sentiment.p_pos
    negvalue = sent.sentiment.p_neg
    return classification, posvalue, negvalue

token = getData('feedconstitutionalpatriot.json')
# token = getData('feedfoodgroups.json')
# token = getData('feedtraveladdiction.json')

# write to csv file
outfile = file('constitutionalpatriots.csv','wb')
# outfile = file('feedfoodgroups.csv','wb')
# outfile = file('feedtraveladdiction.csv','wb')
writer = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)

for message_no, message in enumerate(token):
    # messagenourl = removeURL(message)
    """
    subjectivity = subj_polar(message)[0]
    polarity = subj_polar(message)[1]
    classification = advancedsentiment(message)[0]
    posvalue = advancedsentiment(message)[1]
    negvalue = advancedsentiment(message)[2]
    """
    # write to csv file
    # print pos_tagger(messagenourl)
    # print "%s \t %s  \t %s  \t %s  \t %s \t %s" %(message_no, subjectivity, polarity, classification, posvalue, negvalue)

    # writer.writerow([message_no,subjectivity, polarity, classification, posvalue, negvalue])
    writer.writerow([
        message_no,
        subj_polar(message)[0],
        subj_polar(message)[1],
        advancedsentiment(message)[0],
        advancedsentiment(message)[1],
        advancedsentiment(message)[2]
    ])


outfile.close()


