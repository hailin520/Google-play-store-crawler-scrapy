# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import pymongo
import json
from random import sample
from scrapy.conf import settings
from scrapy.exceptions import DropItem
#from scrapy import log


class MongoDBPipeline(object):
    dictArray = []

    def __init__(self):
        f = open("wordlist.txt", 'r')
        self.dictArray = f.read().split("\r\n")
        f.close()

    def open_spider(self, spider):
        pass
        #self.file = open('ok.json', 'w')

    def close_spider(self, spider):
        pass
        #self.file.close()

    def process_item(self, item, spider):
        if self.canConv(item['numDownloads']) and self.canConv(item['score']) and len(item['description']) > 0:
            if self.formatNumDownloads(item['numDownloads']) >= 1000 and self.formatScore(item['score']) > 3.5 and self.isEnglish(item['description']): 
                filename = item['appid']
                fle = open(filename + '.json', 'w')
                line = json.dumps(dict(item)) + "\n"
                fle.write(line)
                fle.close()
        return item

    def canConv(self, inputString):
        canConvert = False
        cleanString = inputString.replace("+", "").replace(",", "").replace("M", "").replace("k", "").replace(".", "")
        canConvert = cleanString.isdigit()
        return canConvert

    def formatNumDownloads(self, inputString):
        cleanString = inputString.replace("+", "").replace(",", "")
        numericValue = 0
        if "M" in cleanString:
            numericValue = float(cleanString.replace("M", "")) * 1e6
            numericValue = int(numericValue)
        elif "k" in cleanString:
            numericValue = float(cleanString.replace("k", "")) * 1e3
            numericValue = int(numericValue)
        else:
            numericValue = int(cleanString)
        return numericValue


    def formatScore(self, inputString):
        numericValue = float(inputString)
        return numericValue

    def isEnglish(self, inputString):
        isEnglish = True
        wordsInDict = 0
        wordsInDescr = inputString.lower().split(" ")
        
        #wordsInDescr must have at least 10 elements or sample will throw an error
        while len(wordsInDescr) < 10:
            wordsInDescr.append("n0tAW0rd")
        wordSample = sample(wordsInDescr, 10)

        for word in wordSample:
            if word in self.dictArray:
                wordsInDict += 1
        
        if wordsInDict < 3:
            isEnglish = False
        return isEnglish
            
            

        
    


