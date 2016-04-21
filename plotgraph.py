import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import csv

def getDataRow(filename, type):
     x = []
     if type == 'posneg':
          rownum = 3

     with open(filename) as csv_file:
          reader = csv.reader(csv_file)
          for row in reader:
               x.append(row[rownum])
     return x

def normaldistribution():
     """

     h = sorted(x)
     fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
     plt.plot(h, fit)
     plt.hist(h, normed=True)      #use this to draw histogram of your data
     plt.show()                   #use may also need add this
     """
     """
     h = sorted([186, 176, 158, 180, 186, 168, 168, 164, 178, 170, 189, 195, 172,
          187, 180, 186, 185, 168, 179, 178, 183, 179, 170, 175, 186, 159,
          161, 178, 175, 185, 175, 162, 173, 172, 177, 175, 172, 177, 180])  #sorted


     fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
     plt.plot(h, fit)
     plt.hist(h, normed=True)      #use this to draw histogram of your data
     plt.show()                   #use may also need add this
     """

def posneg_piechart(filename):
     x = getDataRow(filename, 'posneg')
     pos = sum(1 for item in x if item == 'pos')
     neg = sum(1 for item in x if item == 'neg')

     labels = 'Pos', 'Neg'
     sizes = [pos, neg]
     colors = ["#E13F29", "#D69A80"]
     explode = (0, 0)    # proportion with which to offset each wedge

     plt.pie(sizes,              # data
             # explode=explode,    # offset parameters
             labels=labels,      # slice labels
             colors=colors,      # array of colours
             autopct='%1.1f%%',  # print the values inside the wedges
             shadow=False,        # enable shadow
             startangle=70       # starting angle
          )
     plt.title('Positive and Negative Sentiment Percentage in Food Groups')
     # plt.tight_layout()
     plt.axis('equal')
     plt.show()

# filename = 'constitutionalpatriots.csv'
# filename = 'feedTEDtranslate.csv'
# filename = 'feedtraveladdiction.csv'
filename = 'feedfoodgroups.csv'
posneg_piechart(filename)