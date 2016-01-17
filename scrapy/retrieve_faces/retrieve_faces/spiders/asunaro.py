# -*- coding: utf-8 -*-

import scrapy
import csv
import urllib
import urlparse

from retrieve_faces.items import FaceItem

class AsunaroSpider(scrapy.Spider):
    name = "asunaro"
    allowed_domains = ['www.seisekiup.net']
    start_urls = ["https://www.seisekiup.net/research/"]
    universities = []
    with open("data/universities.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            universities.append(row[0].decode('utf-8'))

    def start_requests(self):
        yield scrapy.Request("https://www.seisekiup.net/research/m/", callback=self.parse_m)
        yield scrapy.Request("https://www.seisekiup.net/research/l/", callback=self.parse_f)

    def parse_m(self, response):
        # print(response.xpath('//div[@class="prof_box prof_men"]'))
        for box in response.xpath('//div[contains(@class,"prof_men")]'):
            name = box.xpath('.//div[contains(@class,"text_area")]/ul/li[1]/span/text()').extract()[0].strip()
            univ_name = box.xpath('.//div[contains(@class,"text_area")]/ul/li[2]/span/text()').extract()[0].strip()
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
            img_src = box.xpath('.//div[contains(@class,"photo")]/img/@src').extract()[0]
            item['image_urls'] = [urlparse.urljoin(response.url, img_src)]
            yield item
        next_link = response.xpath('//ul[@id="pagenavi"]//a[contains(@class,"link_next")]/@href').extract()
        # self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(urlparse.urljoin(response.url, next_link[0].strip()), callback=self.parse_m)

    def parse_f(self, response):
        # print(response.xpath('//div[@class="prof_box prof_men"]'))
        for box in response.xpath('//div[contains(@class,"prof_lady")]'):
            name = box.xpath('.//div[contains(@class,"text_area")]/ul/li[1]/span/text()').extract()[0].strip()
            univ_name = box.xpath('.//div[contains(@class,"text_area")]/ul/li[2]/span/text()').extract()[0].strip()
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
            img_src = box.xpath('.//div[contains(@class,"photo")]//img/@src').extract()[0]
            item['image_urls'] = [urlparse.urljoin(response.url, img_src)]
            yield item
        next_link = response.xpath('//ul[@id="pagenavi"]//a[contains(@class,"link_next")]/@href').extract()
        # self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(urlparse.urljoin(response.url, next_link[0].strip()), callback=self.parse_f)
