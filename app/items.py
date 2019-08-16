# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GoogleItem(scrapy.Item):
    url = scrapy.Field()
    appid = scrapy.Field()
    score = scrapy.Field()
    Category = scrapy.Field()
    fileSize = scrapy.Field()
    numDownloads = scrapy.Field()
    Updated = scrapy.Field()
    contentRating = scrapy.Field()
    Version = scrapy.Field()
    Android = scrapy.Field()
    privacyPolicy = scrapy.Field()
    privacyPolicyContent = scrapy.Field()
    Price = scrapy.Field()
    description = scrapy.Field()
    permissions = scrapy.Field()
    NumberOfreviews = scrapy.Field()
    continued = scrapy.Field()
    timeStamp = scrapy.Field()
