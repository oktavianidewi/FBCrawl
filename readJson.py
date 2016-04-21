import re
import json
import nltk
from textblob import TextBlob, Blobber
from nltk.corpus import stopwords
from nltk.tokenize import TabTokenizer
from textblob.taggers import NLTKTagger
from textblob.sentiments import NaiveBayesAnalyzer

def getData():
    nama_file = 'feedconstitutionalpatriot.json'
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
    result = 'SubjPolar(subjectivity=%s, polarity=%s)' %(subjectivity, polarity)
    return result

def pos_tagger(message):
    nltk_tagger = NLTKTagger()
    pos_tagged = TextBlob(message, pos_tagger=nltk_tagger)
    return pos_tagged.pos_tags

def advancedsentiment(message):
    # message = unicode(message, 'utf8')
    sent = TextBlob(message, analyzer=NaiveBayesAnalyzer())
    result = sent.sentiment
    return result


token = getData()
for message_no, message in enumerate(token[:10]):
    # messagenourl = removeURL(message)
    print subj_polar(message)
    print advancedsentiment(message)
    # print pos_tagger(messagenourl)
