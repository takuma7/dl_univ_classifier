# -*- coding: utf-8 -*-

import scrapy
import csv
import urllib
import urlparse

from retrieve_faces.items import FaceItem

class YotsuyagakuinSpider(scrapy.Spider):
    name = "yotsuya"
    allowed_domains = ['www.yotsuyagakuin.com']
    start_urls = [
            "http://www.yotsuyagakuin.com/exp/j/?cat=3",
            "http://www.yotsuyagakuin.com/exp/j/?cat=4",
            "http://www.yotsuyagakuin.com/exp/j/?cat=5",
            "http://www.yotsuyagakuin.com/exp/j/?cat=6"
            ]
    universities = []
    with open("data/universities.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            universities.append(row[0].decode('utf-8'))

    def parse(self, response):
        for box in response.xpath('//div[@id="article"]/div[contains(@class,"section")]'):
            univ_name = ''
            dept_name = ''
            for univ_list in box.xpath('dl/dd/ul/li'):
                tmp_univ_text = univ_list.xpath('text()').extract()[0].strip()
                tmp_univ_arr = tmp_univ_text.split(u'大学')
                if len(tmp_univ_arr) != 2:
                    continue
                tmp_univ_name = tmp_univ_arr[0] + u'大学'
                if tmp_univ_name in self.universities:
                    univ_name = tmp_univ_name
                    dept_name = tmp_univ_arr[1]
                    break

            if univ_name == '':
                continue

            item = FaceItem()
            item['name'] = box.xpath('div[contains(@class,"stdnt_data")]/span/text()').extract()[0].strip()
            suffix = box.xpath('div[contains(@class,"stdnt_data")]/text()').extract()[0].split()[0].strip()
            item['gender'] = 'm' if suffix == u'くん' else 'f'
            item['university'] = univ_name
            item['department'] = dept_name
            img_src = box.xpath('div[contains(@class,"stdnt_pht")]//img/@src').extract()[0].strip()
            item['image_urls'] = [img_src]
            yield item
        next_link = response.xpath('//a[contains(@class,"nextpostslink")]/@href').extract()
        self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(next_link[0].strip(), callback=self.parse)
