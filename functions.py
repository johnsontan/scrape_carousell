from os import link
import requests
from lxml.html import fromstring


def reconstruct_posted_ago(arrayNames, arrayDate):
    count = 0
    allIndex = []
    allLinks = []
    returnad = arrayDate
    for an in arrayNames:
        if an.lower() == "new carouseller":
            allIndex.append(count)
        count += 1
    for al in allIndex:
        returnad.insert(al-1,"10 hours ago")    
    return returnad

def reconstruct_seller_name(arrayNames):
    an = arrayNames
    count = 0
    deleteIndexes = []
    for string in arrayNames:
        if string.lower() == "new carouseller":
            deleteIndexes.append(count)
        count += 1
    for index in sorted(deleteIndexes, reverse=True):
        del an[index]
    return an
