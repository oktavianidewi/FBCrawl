import json
import nltk
import os
import string
from dynamicVar import tl_extractor_var

ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words('english'))
NON_ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words()) - ENGLISH_STOPWORDS
STOPWORDS_DICT = {lang: set(nltk.corpus.stopwords.words(lang)) for lang in nltk.corpus.stopwords.fileids()}

def get_language(text):
    words = set(nltk.wordpunct_tokenize(text.lower()))
    return max(((lang, len(words & stopwords)) for lang, stopwords in STOPWORDS_DICT.items()), key = lambda x: x[1])[0]

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
            if len(unusual) <= usual :
                stopwordsdetection = True
            else:
                stopwordsdetection = False
    # print stopwordsdetection, text
    return stopwordsdetection

def countUserdID():
    if 'Store' in data :
        usercount = len(data)-1 # minus Store
    else:
        usercount = len(data)
    return usercount

def getTimeline(*userID):
    pass

english_non_details = {}
def detectLanguageFromUserPosts(userID):
    # checking english post atau bukan?
    if 'timeline' in data[userID] :
        userposts = data[userID]['timeline']
        numOfEnglishPost = 0
        for userpost in userposts:
            # index 12 is for posts
            stopwordsdetection = is_english(userpost[12])
            # print stopwordsdetection, userpost[12]
            if stopwordsdetection:
                numOfEnglishPost += 1
        # print numOfEnglishPost, len(userposts)
        numOfUserPost = len(userposts)
        if numOfEnglishPost > 20:
            status = 'English'
        else:
            status = 'Non-English'
    else:
        status = 'No Posts'
        numOfEnglishPost = 0
        numOfUserPost = 0
    return {"userid":userID,"status":status,"englishpost":numOfEnglishPost,"totalpost":numOfUserPost}
    # return status

def writeToFile(data):
    targetfile = tl_extractor_var()['targetfile']
    print targetfile
    # harus ada pengecekan fileexist atau ga
    """
    isExist = os.path.isfile(targetfile)
    if isExist == True :
        # kalo file exist
        file = open(targetfile, "a")
    else :
        # kalo file not exist
    """
    file = open(targetfile, "w+")
    file.write(json.dumps(data))
    file.close()
    return True

def countValid():
    hitValid = 0
    validUser = []
    for userid in data:
        if 'timeline' in data[userid]:
            hitValid += 1
            validUser.append(userid)
    return validUser

def userEnglishPost():
    resultToWrite = []
    numOfEnglishPostUser = 0
    # get all timeline data
    for userid in data:
        if userid != 'Store':
            print userid
            # english_non[userid] = detectLanguageFromUserPosts(userid)
            result = detectLanguageFromUserPosts(userid)
            if result['status'] == 'English':
                numOfEnglishPostUser += 1
        resultToWrite.append(result)
    writeToFile(resultToWrite)
    print 'jumlah english post user : ', numOfEnglishPostUser
    return numOfEnglishPostUser

# open file
filename = tl_extractor_var()['sourcefile']
with open(filename) as file:
    data = json.load(file)

def checkCrawledUser():
    crawledUser = []
    foldername = 'dataset/20160515_foodgroups backup'
    if os.sep == '/':
        limit = 2
    else:
        limit = 1
    # for root, dirs, files in os.walk(directoryGroup):
    for root in os.walk(foldername):
        arr = root[0].split(os.sep)
        if len(arr) > limit:
            crawledUser.append(unicode(arr[limit]))
    return crawledUser

def countExtracted():
    hitValid = 0
    validUser = []
    with open(tl_extractor_var()['sourcefile'], 'r') as data_file:
        data = json.load(data_file)
    for userid in data:
        if 'timeline' in data[userid]:
            hitValid += 1
            validUser.append(userid)
    return validUser

def untracked():
    # untuk mengetahui selisih antara list of extracted user dengan crawled user di folder
    x = countValid()
    y = checkCrawledUser()

    print sorted(set(x))
    print len(x)
    print sorted(set(y))
    print len(y)

    selisih = list(set(y) - set(x))
    print len(selisih)
    return selisih

writeToFile(untracked())
print untracked()

"""
x = countValid()
a = countExtracted()
print sorted(x)
print sorted(countExtracted())
selisihNotExtracted = list(set(x) - set(a))
print len(selisihNotExtracted)
for i in selisihNotExtracted:
    print i
"""