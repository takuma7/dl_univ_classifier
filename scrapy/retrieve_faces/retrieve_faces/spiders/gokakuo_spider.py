# -*- coding: utf-8 -*-

import scrapy
import csv
import urllib
import urlparse

from retrieve_faces.items import FaceItem

class GokakuoSpider(scrapy.Spider):
    name = "gokakuo"
    allowed_domains = ['www.gokaku-o.com']
    start_urls = [
            "http://www.gokaku-o.com/search/tokyo/",
            "http://www.gokaku-o.com/search/kanagawa/",
            "http://www.gokaku-o.com/search/chiba/",
            "http://www.gokaku-o.com/search/saitama/"
            ]
    universities = []
    with open("data/universities.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            universities.append(row[0].decode('utf-8'))

    def parse(self, response):
        for tutor in response.xpath('//table[contains(@class,"list_tutor")]'):
            univ_text = tutor.xpath('./tbody/tr[1]/td[2]/text()').extract()[0].strip()
            univ_arr  = univ_text.split(u'大学')
            univ_name = univ_arr[0] + u'大学'
            if univ_name not in self.universities:
                continue

            item = FaceItem()
            # item['name'] = tutor.xpath('a/text()').extract()[0].strip()
            item['gender'] = 'm' if tutor.xpath('./tbody/tr[4]/td[2]/text()').extract()[0].strip() == u'男' else 'f'
            item['university'] = univ_name

            if len(univ_arr) > 1:
                dept_name = univ_arr[1].split(u'学部')[0] + u'学部'
                item['department'] = dept_name

            img_src = tutor.xpath('./tbody/tr[1]/td[3]/img/@src').extract()[0]
            item['image_urls'] = [img_src]
            yield item

