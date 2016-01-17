# -*- coding: utf-8 -*-

import scrapy
import csv
import urllib
import urlparse

from retrieve_faces.items import FaceItem

class UmasterSpider(scrapy.Spider):
    name = "umaster"
    allowed_domains = ['www.u-master.net']
    universities = []
    with open("data/universities.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            universities.append(row[0].decode('utf-8'))

    def start_requests(self):
        yield scrapy.Request("http://www.u-master.net/tut_info/?cat=2", callback=self.parse_m)
        yield scrapy.Request("http://www.u-master.net/tut_info/?cat=3", callback=self.parse_f)

    def parse_m(self, response):
        # print(response.xpath('//div[@class="prof_box prof_men"]'))
        for box in response.xpath('//table[contains(@class,"man")]'):
            name = box.xpath('.//div[contains(@class,"namae")]/text()').extract()[0].strip()
            univ_name = box.xpath('.//div[contains(@class,"gakkou")]/text()').extract()[0].strip()
            if univ_name not in self.universities:
                # self.logger.debug(u'skip: ' + univ_name)
                continue
            else:
                # self.logger.debug(u'pass: ' + univ_name)
                pass

            item = FaceItem()
            item['name'] = name
            item['gender'] = 'm'
            item['university'] = univ_name
            img_src = box.xpath('./tbody/tr[1]/td[1]/img/@src').extract()[0]
            item['image_urls'] = [img_src]
            yield item
        next_link = response.xpath('//a[contains(@class,"next")]/@href').extract()
        # self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(urlparse.urljoin(response.url, next_link[0].strip()), callback=self.parse_m)

    def parse_f(self, response):
        # print(response.xpath('//div[@class="prof_box prof_men"]'))
        for box in response.xpath('//table[contains(@class,"woman")]'):
            name = box.xpath('.//div[contains(@class,"namae")]/text()').extract()[0].strip()
            univ_name = box.xpath('.//div[contains(@class,"gakkou")]/text()').extract()[0].strip()
            if univ_name not in self.universities:
                # self.logger.debug(u'skip: ' + univ_name)
                continue
            else:
                # self.logger.debug(u'pass: ' + univ_name)
                pass

            item = FaceItem()
            item['name'] = name
            item['gender'] = 'f'
            item['university'] = univ_name
            img_src = box.xpath('./tbody/tr[1]/td[1]/img/@src').extract()[0]
            item['image_urls'] = [img_src]
            yield item
        next_link = response.xpath('//a[contains(@class,"next")]/@href').extract()
        # self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(urlparse.urljoin(response.url, next_link[0].strip()), callback=self.parse_f)

