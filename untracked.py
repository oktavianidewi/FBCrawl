import savReaderWriter as sav
# from tl_extractor import untracked
from dynamicVar import untracked_var
import shutil
import os
import json
"""
def moveUntracked():
    foldernamearr = untracked()
    for foldername in foldernamearr:
        shutil.move("dataset/20160515_foodgroups/"+foldername, "dataset/20160515_foodgroups_untracked/")
"""

def directoryexist(directory):
    # create folder
    # directory = userid
    if not os.path.exists(directory):
        os.makedirs(directory)
    directoryIsExist = True
    return directoryIsExist

def moveEnglishPost():
    source = untracked_var()['sourcefile']
    sourcedir = untracked_var()['sourcedir']
    targetdir = untracked_var()['targetdir']
    with open(source, 'r') as data_file:
        x = json.load(data_file)
        for row in x:
            if row['englishpost'] > 20:
                # moving process
                print row['userid']
                # directoryexist(targetdir+'/'+row['userid'])
                try:
                    shutil.move(sourcedir+"/"+row['userid'], targetdir)
                except Exception, e:
                    continue

moveEnglishPost()

def readSavGroupUser():
    userarr = {}
    sourcefile = 'dataset/271_user_other.sav'
    # targetfile = '271_user_other.json'

    with sav.SavReader(sourcefile) as reader:
        records = reader.all()
    for i in records:
        userarr[i[3]] = i[5]
    # unique = list(set(userarr))
    return userarr

def separateIntoGroup():
    userGroup = readSavGroupUser()
    print userGroup
    for userid in userGroup:
        print userid+': '+userGroup[userid]
        directoryexist("dataset/"+userGroup[userid])
        try:
            shutil.move("dataset/20160520_271_user/"+userid, "dataset/20160520_271_user/"+userGroup[userid])
        except Exception, e:
            continue
    # print userGroup

# separateIntoGroup()
