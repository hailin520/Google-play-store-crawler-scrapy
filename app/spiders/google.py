# -*- coding: utf-8 -*-
import re
import json
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from app.items import GoogleItem


class GoogleSpider(CrawlSpider):
    name = "google"
    privacyPolicy = ""
    allowed_domains = ["play.google.com"]
    start_urls = [
        'http://play.google.com/',
        'https://play.google.com/store/apps/details?id=com.instagram.android'
    ]

    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details",)), callback='parse_app', follow=True),
    ]

    def __init__(self, *a, **kw):
        super(GoogleSpider, self).__init__(*a, **kw)

    def parse_app(self, response):

    	item = GoogleItem()
    	item['url'] = response.url

        item['appid'] = response.url.split("?id=")[-1].split("&")[0]

        item['score'] = response.xpath("//div[@class='BHMmbe']").xpath("text()").get(default='not-found')

        item['Category'] = response.xpath("//span[@class='T32cc UAO9ie'][2]/a[@class='hrTbp R8zArc']/text()").get(default='not-found')

        fileSizeTextArray = response.xpath("//div[contains(text(), 'Size')]/..//text()").getall() 
        item['fileSize'] = fileSizeTextArray[1] if len(fileSizeTextArray) > 0 else 'not-found'

        installsTextArray = response.xpath("//div[contains(text(), 'Installs')]/..//text()").getall()
    	item['numDownloads'] = installsTextArray[1] if len(installsTextArray) > 0 else 'not-found' 

        updatedTextArray = response.xpath("//div[contains(text(), 'Updated')]/..//text()").getall() 
        item['Updated'] = updatedTextArray[-1] if len(updatedTextArray) > 0 else 'not-found'

        contentRatingTextArray = response.xpath("//div[contains(text(), 'Content Rating')]/..//text()").getall() 
        item['contentRating'] = contentRatingTextArray[1] if len(contentRatingTextArray) > 0 else 'not-found'

        versionTextArray = response.xpath("//div[contains(text(), 'Current Version')]/..//text()").getall() 
        item['Version'] = versionTextArray[1] if len(versionTextArray) > 0 else 'not-found'

        androidTextArray = response.xpath("//div[contains(text(), 'Requires Android')]/..//text()").getall() 
        item['Android'] = androidTextArray[1] if len(androidTextArray) > 0 else 'not-found'

        item['privacyPolicy'] = response.xpath("//a[contains(text(), 'Privacy Policy')]").xpath("@href").get(default='not-found')

        item['Price'] = response.xpath("//button[contains(text(), 'Buy')]/text()").get(default='free').split(" ")[0]

        item['description'] = " ".join(response.xpath("//div[@class='DWPxHb']/span/div[1]/text()").getall())

        item['permissions'] = []

        item['NumberOfreviews'] = response.xpath("//div[@class='dNLKff']/c-wiz/span[@class='AYi5wd TBRnV']/span[1]/text()").get(default='not-found')

        item['continued'] = True

        doc_url = "https://play.google.com/store/xhr/getdoc"
        doc_form = {"ids": item['appid'], "xhr": '1'}
        yield FormRequest(doc_url, callback=self.parse_doc, formdata=doc_form, meta={'item': item})
	

    def parse_doc(self, response):
        item = response.meta['item']
        data = re.findall("\{.*\}", response.body, re.S)
        pat = re.findall(",\[\[.*", data[0], re.S)
        if len(pat) > 0:
            pers = re.findall("\[\".*\",\d\]", pat[0])
            for per in pers:
                text = json.loads(per)[0]
                if text not in item['permissions']:
                    item['permissions'].append(text)

            for key, value in item.items():
                if type(value) == list:
                    item[key] = [x.encode('utf-8') for x in value]
                if type(value) == str or type(value) == unicode:
                    item[key] = value.encode('utf-8')
            yield item
