from tl_extractor import untracked
import shutil

foldernamearr = untracked()
for foldername in foldernamearr:
    shutil.move("dataset/20160515_foodgroups/"+foldername, "dataset/20160515_foodgroups_untracked/")