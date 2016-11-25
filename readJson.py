# coding: utf-8
import re
import json
import nltk
from textblob import TextBlob, Blobber
from textblob.taggers import NLTKTagger
from textblob.sentiments import NaiveBayesAnalyzer
import csv
from nltk.tokenize import RegexpTokenizer
import string

"""
# tambahan : 08.23.2016
1. encode/decode the posts
tweet = unicode(tweet)
result = tweet.decode('unicode_escape').encode('ascii', 'ignore')
2. Replace usernames mentioned in the text with the string literal, 'USER'
result = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_.]))@([A-Za-z]+[A-Za-z0-9]+)', 'USER', result)
3. Replace URLs with the string 'URL'
result = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL', result)
4. Remove Backslash character
result = result.replace('\', '')

"""

ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words('english'))
NON_ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words()) - ENGLISH_STOPWORDS
STOPWORDS_DICT = {lang: set(nltk.corpus.stopwords.words(lang)) for lang in nltk.corpus.stopwords.fileids()}

def is_english(text):
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    text = text.lower()
    words = set(nltk.wordpunct_tokenize(text))
    stopwordsdetection = len(words & ENGLISH_STOPWORDS) > len(words & NON_ENGLISH_STOPWORDS)

    if not text:
        # print 'kosong'
        stopwordsdetection = False
    else:
        if not stopwordsdetection:
            textsplit = text.split(" ")
            # text_vocab = set(w.lower() for w in textsplit if w.lower().isalpha())
            text_vocab = set(" ".join("".join([" " if ch in string.punctuation else ch for ch in text.lower()]).split()).split())
            unusual = text_vocab.difference(english_vocab)
            usual = len(text_vocab)-len(unusual)
            if len(unusual) > 3:
                stopwordsdetection = False
            else:
                stopwordsdetection = True
    # print stopwordsdetection, text
    return stopwordsdetection

def getData(nama_file):
    isArray = type(nama_file).__name__ == 'list'
    json_data = {}
    dict = {}
    if isArray == True :
        # read multiple files
        for filename in nama_file:
            group = filename.split('/')[1].split('.')[0]
            with open(filename) as file:
                dict[group] = json.load(file)
            json_data.update(dict)
    else:
        with open(nama_file) as data_file:
            group = nama_file.split('/')[1].split('.')[0]
            dict[group] = json.load(data_file)
            json_data = dict
            # write to csv file

    if isArray == True:
        simpan = open('2allpost_subj_pol.csv','wb')
    else:
        # simpan = open(nama_file.split('.')[0]+'_subj_pol.csv','wb')
        simpan = open('1english_TEDtranslate_subj_pol.csv','wb')

    writer = csv.writer(simpan,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['UserID','GroupName','Ori_Post','PreProPost','Ori_Subj','Subj','Ori_Pol','Pol'])

    for group in json_data:
        if group == 'english_traveladdiction':
            groupname = 'Travel Addiction'
        elif group == 'english_foodgroup':
            groupname = 'Foodgroup'
        elif group == 'english_Hiking With Dogs':
            groupname = 'Hiking With Dogs'
        elif group == 'english_Jazzmasters&Jaguars':
            groupname = 'Jazzmasters&Jaguars'
        elif group == 'english_Like For Like Promote Your Business':
            groupname = 'Like For Like Promote Your Business'
        elif group == 'english_constitutionalpatriot_dw':
            groupname = 'Constitutional Patriots'
        elif group == 'english_TEDtranslate':
            groupname = 'TEDtranslate'

        grouped = json_data[group]
        for userid in grouped:
            print userid
            if "timeline" in grouped[userid]:
                timeline = grouped[userid]['timeline']
                for posts in timeline :
                    singlepost = posts[12].encode('ascii', 'ignore').decode('ascii')
                    englishtext = is_english(posts[12])
                    print englishtext, singlepost
                    if singlepost and englishtext :
                        z = removeURL(singlepost)

                        subj_pol_score = subj_polar(z)
                        # pos_neg_score = advancedsentiment(z)

                        subj_pol_score_normal = subj_polar(singlepost)
                        # pos_neg_score_normal = advancedsentiment(singlepost)

                        writer.writerow([
                            userid,
                            groupname,
                            singlepost,
                            z,
                            subj_pol_score_normal[0], # subjectivity
                            subj_pol_score[0], # subjectivity
                            subj_pol_score_normal[1], # polarity
                            subj_pol_score[1], # polarity
                        ])
    simpan.close()
    # return token

# hapus tanda >>> .... , tulisan Continue Reading, See Translation, See More, remove bahasa non Inggris

def removeSymbol(message):
    regex = "[^\w'!]|._><"
    cln = re.sub(regex, " ", message).rstrip().lstrip()
    return cln

def removeURL(message):
    # remove URLs
    messageNoUrl = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', 'URL', message)
    return messageNoUrl

def removeMention(message):
    regex = '(?<=^|(?<=[^a-zA-Z0-9-_.]))@([A-Za-z]+[A-Za-z0-9]+)'
    messageNoMention = re.sub(regex, 'USER', message)
    return messageNoMention

def removeSongTitle(message, type):
    if type == 'apple':
        woTitle = re.sub(r'(?<=Listen to)(.*)(?=by)', ' TITLE ', message)
        result = re.sub(r'(?<=by)(.*)(?=on)', ' NAME ', woTitle)
    elif type == 'klove':
        woTitle = re.sub(r'(.*)(?= by )', 'TITLE', message)
        result = re.sub(r'(?<=by)(.*)(?=now)', ' NAME ', woTitle)
    return result

def subj_polar(message):
    blob = TextBlob(message)
    polarity  = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
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

"""
# 08.23.2016 : jadiin komen
nama_file = 'extracted/english_TEDtranslate.json'
nama_file_array = [
    'extracted/english_foodgroup.json',
    'extracted/english_traveladdiction.json',
    'extracted/english_TEDtranslate.json',
    'extracted/english_constitutionalpatriot_dw.json'
]

token = getData(nama_file_array)

"""

"""
'extracted/english_constitutionalpatriot.json'
'extracted/english_Hiking With Dogs.json',
'extracted/english_Jazzmasters&Jaguars.json',
'extracted/english_Like For Like Promote Your Business.json',
"""