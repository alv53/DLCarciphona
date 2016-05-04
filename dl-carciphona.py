#!/usr/bin/python
import sys
import os
import requests
import shutil

# Returns the total number of volumes of Carciphona
def GetNumVols():
    #TODO: Maybe make this based on web scraping the selecter for volume.
    # Might be extraneous though, as a new volume comes out very infrequently.
    return 5

# Add leading 0s to an integer, and convert it to a string
def AddLeadingChars(value, maxLen):
    returnVal = str(value)
    # Loop to add characters
    while len(returnVal) < maxLen:
        returnVal = "0" + returnVal
    return returnVal

# Gets the full url of the desired image
def GetImgUrl(url, vol, fileName):
    return url + "/_pages/" + str(vol) + "/" + fileName

url = "http://carciphona.com"
ext = ".jpg"
covers = ["coverleft", "coverright"]
numVols = GetNumVols()

# Create directory
dirName = "Carciphona"
if not os.path.exists(dirName):
    print "Creating directory " + dirName
    os.makedirs(dirName)

for vol in range(1,numVols + 1):
    # Create the volume directory
    volName = dirName + '/' + dirName + "-" + str(vol)
    if not os.path.exists(volName):
        print "Creating directory " + volName
        os.makedirs(volName)

    # Download cover pages (left and right)
    for cover in covers:
        fileName = cover + ext
        urlToDl = GetImgUrl(url, vol, fileName)
        dest = volName + '/' + fileName
        if not os.path.exists(dest):
            print "Downloading " + urlToDl + " to " + dest
            res = requests.get(urlToDl, stream=True)
            with open(dest, "wb") as out_file:
                shutil.copyfileobj(res.raw, out_file)
    # Download all the images now
    currPage = 1
    while True:
        fileName = AddLeadingChars(currPage, 3) + ext
        urlToDl = GetImgUrl(url, vol, fileName)
        dest = volName + '/' + fileName
        if not os.path.exists(dest):
            print "Downloading " + urlToDl + " to " + dest
            res = requests.get(urlToDl, stream=True, allow_redirects=False)
            # if we are redirected to homepage, we have run out of pages
            if res.status_code == 302:
                break
            with open(dest, "wb") as out_file:
                shutil.copyfileobj(res.raw, out_file)
        currPage += 1
