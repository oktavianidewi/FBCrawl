import os
import sys
from import2csv import compareWithPreviousUser, findIndex
from dynamicVar import stoppeduserid, crawler_win_var
import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import time
import json
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# import BeautifulSoup
# import json
# from selenium.webdriver.common.action_chains import ActionChains
# import random

date = time.strftime('%Y%m%d',time.localtime(time.time()))
groupname = crawler_win_var()['groupname']

def directoryexist(directory):
    # create folder
    # directory = userid
    if not os.path.exists(directory):
        os.makedirs(directory)
    directoryIsExist = True
    return directoryIsExist

def savepage(type, userid):
    if crawler_win_var()['info'] == 'additionaluser':
        # directory is based on userid
        if '?' in userid:
            directory = string.replace(userid, '?', '#')
        else:
            directory = userid
        userid = string.replace(userid, '?', '#')
    elif crawler_win_var()['info'] == 'untrackeduser':
        directory = userid.rstrip('\n')
    else:
        # directory is based on userid
        directory = userid.rstrip('\n')
    # checking directory
    checkgroupname = directoryexist('dataset/photos/'+date+'_'+groupname)
    checkdirectory = directoryexist('dataset/photos/'+date+'_'+groupname+'/'+directory)
    page_html = driver.page_source
    page_html_file = open('dataset/photos/'+date+'_'+groupname+'/'+directory+'/'+type+'_'+userid+'.html', 'w')
    page_html_file.write(page_html)
    page_html_file.close()

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def scrollLikePage(current_url, userid):
    # scroll until got 100 top-likes
    # https://www.facebook.com/profile.php?id=100008397645072&sk=likes
    # https://www.facebook.com/rido.monthazeri/likes
    if 'profile.php?id=' in current_url:
        likes_url = current_url+'&sk=likes'
    else:
        likes_url = current_url+'/likes'
    driver.get(likes_url)
    time.sleep(1)
    current_url_after_redirect = driver.current_url

    if current_url_after_redirect == likes_url :
        background = driver.find_element_by_css_selector("body")
        for i in range(1, 20):
            time.sleep(0.7)
            background.send_keys(Keys.SPACE)
    savepage('likes', userid)
    # rlog(userid, likes_url)

def scrollTimelinePage(current_url, userid):
    background = driver.find_element_by_css_selector("body")
    # Better to stop here. Or it may have exception at background.send_keys(Keys.SPACE).
    # time.sleep(3)

    # Prevent invalid page.
    try:
        driver.find_element_by_id('fb-timeline-cover-name')
    except Exception, e:
        # save these URLs
        rlog('timeline','invalid page : %s ' %(e),0, userid)

    try:
        # set default scrolllimit
        scrolllimit = 4
        stop = False
        yearlimit = 2015
        startTag = 0
        recordOfTagNum = []
        sleeptime = 3
        constantlength = False
        while (stop == False and constantlength == False):
            # do scrolling
            for i in range(1, scrolllimit):
                background.send_keys(Keys.SPACE)
            time.sleep(sleeptime)

            # find elements by class
            tag = driver.find_elements_by_css_selector('._5ptz')

            # antisipasi kalo user punya banyak post
            # antisipasi kalo user punya post banyak
            if tag.__len__() > 350 :
                stop = True
            else:
                stop = False

            # antisipasi post user sedikit dan tahunnya > yearlimit
            countOfMax = [a for a in recordOfTagNum if a == max(recordOfTagNum)]
            recordOfTagNum.append(tag.__len__())
            if len(recordOfTagNum) > 5:
                print recordOfTagNum
                # compare
                # True and True
                if (recordOfTagNum[0] == recordOfTagNum[recordOfTagNum.index(max(recordOfTagNum))]) and (len(countOfMax) > 10) :
                    constantlength = True
                elif (recordOfTagNum[0] != recordOfTagNum[recordOfTagNum.index(max(recordOfTagNum))]) and (len(countOfMax) > 10) :
                    constantlength = True
                elif (recordOfTagNum[0] == recordOfTagNum[recordOfTagNum.index(max(recordOfTagNum))]) and (len(countOfMax) < 10) :
                    constantlength = True
                else:
                    constantlength = False

            # antisipasi kalo loading tiba2 berhenti

            # nilai start dinamis
            for x in range(startTag, tag.__len__()):
                postyear = (tag[x].get_attribute("title")).split(" ")
                tahun = int(postyear[3])
                print tag[x].get_attribute("title")
                print x
                if yearlimit <= tahun:
                    stop = False
                else:
                    stop = True
                startTag = x+1
        savepage('timeline', userid)
    except TimeoutException:
        rlog('timeline','keterangan timeout : %s' %(e),startrow, userid)
    # rlog(userid, url)

    # https://www.facebook.com/daniela.andrisani.1/photos_albums

def scrollPhotos(current_url, userid):
    # browse Photos page
    # value collection_token= can be any
    # https://www.facebook.com/profile.php?id=100006257565287&sk=photos&collection_token=100006257565287%3A2305272732%3A6
    # https://www.facebook.com/profile.php?id=100011268031177&sk=photos&collection_token=100011268031177%3A2305272732%3A6
    # https://www.facebook.com/profile.php?id=100010520260602&sk=photos&collection_token=100006257565287%3A2305272732%3A6
    if 'profile.php?id=' in current_url:
        # kadang userid nya ketika di url berubah jadi id lain
        photo_url = current_url+'&sk=photos&collection_token=100006257565287%3A2305272732%3A6'
    else:
        # https://www.facebook.com/Adventure.Cyclist/photos_albums
        photo_url = current_url+'/photos_albums'
    # open page based on url
    print photo_url
    driver.get(photo_url)
    # save webpage
    savepage("photos", userid)

def scrollAboutPage(current_url, userid):
    # browse ABOUT page
    if 'profile.php?id=' in current_url:
        # https://m.facebook.com/profile.php?id=114407042245292&sk=about
        # kadang userid nya ketika di url berubah jadi id lain
        username = current_url.split('=')[1].split('&')[0]
        about_url = 'https://m.facebook.com/profile.php?id='+username+'&sk=about'
    else:
        username = current_url.split('/')[3]
        about_url = 'https://m.facebook.com/'+username+'/about'
    # open page based on url
    print about_url
    driver.get(about_url)
    # save webpage
    savepage("about", userid)

# rlog('timeline','success',startrow, userid)
def rlog(type, status, i, userid):
    # Record the start time.
    starttime = datetime.datetime.now()
    filename = "log_"+date+".txt"
    teks = "%s,%s,%s,%s,%s \n" % (type, status, starttime, i, userid)

    # harus ada pengecekan fileexist atau ga
    isExist = os.path.isfile(filename)
    if isExist == True :
        # kalo file exist
        file = open('log/'+filename, "a")
    else :
        # kalo file not exist
        file = open('log/'+filename, "w+")
    file.write(teks)
    file.close()
    return True

def lastCheckedNum(logfilename):
    # menentukan startrow dari file log
    checkeduser = []
    with open(logfilename, 'r') as row:
        x = row.readlines()
        if len(x) > 1:
            for baris in x:
                row = baris.split(',')[3]
                if row not in checkeduser:
                    checkeduser.append(row)
            start = max(checkeduser)
        else:
            start = 1
    return start

import pandas as pd
import numpy as np
import csv

arr_header = []

if __name__ == '__main__':
    urls = []
    reload(sys)
    sys.setdefaultencoding('utf-8')
    baseurl = 'www.facebook.com/'

    print crawler_win_var()
    if crawler_win_var()['info'] == 'additionaluser':
        # data_file = open('dataset/271_user.json', 'r')
        # xx = json.load(data_file)

        csvfile = open('header_type_json_timeline.csv', 'rb')
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        arr_header = [row[0] for row in csvreader]


        # content
        presentFile = 'extracted/english_TEDtranslate_new.json'
        data_file = open(presentFile)
        json_data = json.load(data_file)
        alluser = []

        for username in json_data:
            if 'timeline' in json_data[username]:
                for row in json_data[username]['timeline']:
                    row.insert(0, username)
                    alluser.append(row[:len(arr_header)])
        df = pd.DataFrame(alluser, columns=arr_header)
        # print df.iloc[:[0,len(arr_header)]]
        # df = df[list(df.columns[0:len(arr_header)])]
        # print df['PostTextPolarity']
        # df = pd.DataFrame(alluser, columns=arr_header)
        getuserurl = {'UserID':np.min, 'UserURL':np.min, 'UserName':np.min}
        aggr_df = df.groupby(['UserID'], sort=True).agg(getuserurl)
        urls = aggr_df[['UserURL', 'UserID']].values
        """
        # file dari grup general user
        GU_file = open('dataset/GU.txt', 'r')
        xx = GU_file.read().splitlines()

        startrow = 0
        endrow = len(xx)
        # endrow = xx.__len__()
        for url in range(startrow, endrow):
            getuserurl = xx[url]
            if '?fref' in getuserurl:
                getuserurl = getuserurl.split('?fref')[0]
            urls.append(getuserurl)
        """
    elif crawler_win_var()['info'] == 'untrackeduser':
        # xx = [u'1477444162534966', u'10204701900000114', u'10152552286655763', u'4887145112253', u'10203652568497538', u'1416634351936875', u'10152384355448810', u'10152381325868303', u'837326856279472', u'10203137783071697', u'10154349884460024', u'10203834055163514', u'528913373883958', u'10204692203517335', u'10107202862038624', u'10202950116666208', u'10152412589795849', u'10152599095188106', u'10152014712611828', u'10203748073087617', u'10152908300611754', u'10204024990125052', u'1262916743734247', u'10152848115570550', u'10153262842783438', u'828857630459305', u'679755542100676', u'10152499848757953', u'10154303667523984', u'10152217636427935', u'10152539243109066', u'10102006073120185', u'10153040663402356', u'1481118935474433', u'10154361443330013', u'10152401307962269', u'574194772708824', u'752652898105077', u'1436294530016505', u'10152157612109011', u'1197185806964764']
        xx = crawler_win_var()['untrackedarr']
        print xx
        """
        with open('dataset/20160515_foodgroups_un.json', 'r') as data_file:
            xx = json.load(data_file)
        """
        startrow = 0
        endrow = xx.__len__()
        for idx in range(startrow, endrow):
            getuserid = xx[idx]
            urls.append(getuserid)
    else:
        # get userid from .csv file
        urls = []
        readfile = compareWithPreviousUser()
        print urls

        if findIndex(stoppeduserid) :
            startrow = findIndex(stoppeduserid)
        else:
            startrow = 0
        endrow = readfile.__len__()

        for idx in range(startrow, endrow):
            getuserid = readfile[idx]
            urls.append(getuserid)

    print urls
    # driver init
    driver = webdriver.Chrome()
    # Set the timeout for the driver and socket.
    driver.set_page_load_timeout(20)
    # socket.setdefaulttimeout(10)

    # First, login.
    driver.get("https://www.facebook.com/login.php")
    # time.sleep(3)
    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys(crawler_win_var()['email'])
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("pass").send_keys(crawler_win_var()['password'])
    driver.find_element_by_id("loginbutton").click()
    # Better wait for several seconds.
    # time.sleep(3)

    # Maybe the login failed. It may turn to the login page again.
    # you may need to load again.
    if 'login' in driver.current_url:
        driver.close()

    # visit the url based on urls
    idx = 0
    userid = 0
    for useridraw, userid in urls:
        time.sleep(1)
        if crawler_win_var()['info'] == 'additionaluser':
            url = useridraw
            idx += 1
            # userid = useridraw.split('/')[3]
            userid = str(userid)
        elif crawler_win_var()['info'] == 'untrackeduser':
            userid = useridraw.rstrip('\n')
            url = baseurl+userid
        else:
            userid = useridraw.rstrip('\n')
            url = baseurl+userid

        print(url)
        # you should know how long you scroll in this timeline - for set the timeout
        # Print the start time.
        print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
        # Wait 3 seconds for the browser loading the Webpage.
        # time.sleep(3)

        driver.get(url)
        # cari scc selector yg ada di halaman likes. supaya bisa discroll
        # tabs = ['timeline', 'likes', 'about']
        current_url = driver.current_url

        # source nya : english_dataset
        # scroll friends di link :
        # scroll photos di link :
        try:
            scrollPhotos(current_url, userid)
            rlog('photos','success',idx, userid)
        except Exception, e:
            rlog('photos','failed : %s' %(e),idx, userid)
            continue