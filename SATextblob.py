from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
from nltk.corpus import stopwords

nama_file = 'feedconstitutionalpatriot.txt'
messages = [line.rstrip() for line in open(nama_file)]

def advancedsentiment(message):
    # message = unicode(message, 'utf8')
    # blob = TextBlob(message)
    # blob.tags
    # blob.noun_phrases
    """
    for sentence in blob.sentences:
        print sentence.sentiment.polarity
        print sentence.sentiment.subjectivity
    """

    sent = TextBlob(message, analyzer=NaiveBayesAnalyzer())
    classification = sent.sentiment.classification
    print sent.sentiment.p_pos
    print sent.sentiment.p_neg


def simplesentiment(message):
    blob = TextBlob(message)
    print blob.sentiment

for message_no, message in enumerate(messages[:10]):
    # print message_no, message
    print message
    print advancedsentiment(message)
    # print simplesentiment(message)

# with open(nama_file) as data_file:
#    text = data_file.read()