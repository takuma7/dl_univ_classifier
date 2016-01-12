# -*- coding: utf-8 -*-

import scrapy
import csv
import urllib
import urlparse

from retrieve_faces.items import FaceItem

class TomonokaiSpider(scrapy.Spider):
    name = "tomonokai"
    allowed_domains = ['www.tomonokai.net']
    start_urls = ["http://www.tomonokai.net/teacher/?_search%5Bgender%5D=%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%AA%E3%81%84&_search%5Bis-thumbnail%5D=yes&_search%5Bcollege_type%5D=%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%AA%E3%81%84&_search%5Bhighschool_for_search%5D%5B0%5D=%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%AA%E3%81%84&leading_subject"]

    def parse(self, response):
        for tr in response.xpath('//table[@class="teacher-text-swipe"]/tbody/tr'):
            img_cell = tr.xpath('td[1]')
            name_cell = tr.xpath('td[2]')
            univ_cell = tr.xpath('td[3]')
            item = FaceItem()
            item['name'] = name_cell.xpath('a/text()').extract()[0].strip()
            item['gender'] = 'm' if img_cell.xpath('p/@class').extract()[0].strip() == 'man' else 'f'
            item['university'] = univ_cell.xpath('text()').extract()[0]
            img_src = img_cell.xpath('p/img/@src').extract()[0]
            item['image_urls'] = [urlparse.urljoin(response.url, img_src)]
            yield item
        next_link = response.xpath('//ul[@class="page_navi"]/li[@class="current"]/following-sibling::li[1]/a/@href').extract()[0].strip()
        self.logger.debug(next_link)
        if next_link:
            yield scrapy.Request(next_link, callback=self.parse)
