# -*- coding: utf-8 -*-

import scrapy
import csv
import urllib
import urlparse

from retrieve_faces.items import FaceItem

class SeisekiupSpider(scrapy.Spider):
    name = "seisekiup"
    allowed_domains = ['www.seisekiup.info']
    start_urls = ["http://www.seisekiup.info/fight/search/cat1"]
    universities = []
    with open("data/universities.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            universities.append(row[0].decode('utf-8'))

    def start_requests(self):
        yield scrapy.Request("http://www.seisekiup.info/fight/search/cat1/", callback=self.parse_m)
        yield scrapy.Request("http://www.seisekiup.info/fight/search/cat2/", callback=self.parse_f)

    def parse_m(self, response):
        for person in response.xpath('//div[@class="searchArea"]'):
            univ_text = person.xpath('.//li[@class="college"]//text()').extract()[0].strip()
            univ_arr = univ_text.split(u'大学')
            univ_name = univ_arr[0].strip() + u'大学'
            if len(univ_arr) != 2:
                # self.logger.debug(u'skip: ' + univ_name)
                continue
            dept_name = univ_arr[1].strip()
            if univ_name not in self.universities:
                # self.logger.debug(u'skip: ' + univ_name)
                continue
            else:
                # self.logger.debug(u'pass: ' + univ_name)
                pass
            item = FaceItem()
            item['name'] = person.xpath('.//li[@class="name"]/text()').extract()[0].strip()
            item['gender'] = 'm'
            item['university'] = univ_name
            item['department'] = dept_name
            img_src = person.xpath('.//li[@class="photo"]/img/@src').extract()[0]
            # item['image_urls'] = [urlparse.urljoin(response.url, img_src)]
            item['image_urls'] = [img_src]
            yield item
        next_link = response.xpath('//a[@class="link_next"]/@href').extract()
        # self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(next_link[0].strip(), callback=self.parse_m)

    def parse_f(self, response):
        for person in response.xpath('//div[@class="searchArea"]'):
            univ_text = person.xpath('.//li[@class="college"]//text()').extract()[0].strip()
            univ_arr = univ_text.split(u'大学')
            univ_name = univ_arr[0].strip() + u'大学'
            if len(univ_arr) != 2:
                # self.logger.debug(u'skip: ' + univ_name)
                continue
            dept_name = univ_arr[1].strip()
            if univ_name not in self.universities:
                # self.logger.debug(u'skip: ' + univ_name)
                continue
            else:
                # self.logger.debug(u'pass: ' + univ_name)
                pass
            item = FaceItem()
            item['name'] = person.xpath('.//li[@class="name"]/text()').extract()[0].strip()
            item['gender'] = 'f'
            item['university'] = univ_name
            item['department'] = dept_name
            img_src = person.xpath('.//li[@class="photo"]/img/@src').extract()[0]
            # item['image_urls'] = [urlparse.urljoin(response.url, img_src)]
            item['image_urls'] = [img_src]
            yield item
        next_link = response.xpath('//a[@class="link_next"]/@href').extract()
        # self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(next_link[0].strip(), callback=self.parse_f)
