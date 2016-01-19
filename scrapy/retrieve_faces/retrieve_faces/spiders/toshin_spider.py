# -*- coding: utf-8 -*-

import scrapy
import csv
import urllib
import urlparse

from retrieve_faces.items import FaceItem

class ToshinSpider(scrapy.Spider):
    name = "toshin"
    allowed_domains = ['www.toshin.com']
    base_urls = [
            "http://www.toshin.com/taikenki/2013/box_list.php",
            "http://www.toshin.com/taikenki/2014/box_list.php",
            "http://www.toshin.com/taikenki/box_list.php"
            ]
    universities = []
    with open("data/universities.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            universities.append(row)

    def start_requests(self):
        for university in self.universities:
            for base_url in self.base_urls:
                query = {'page': 0, 'data':(u'{"select_univ_school":"'+university[0].decode('utf-8')+u'"}').encode('utf-8')}
                url = base_url + '?' + urllib.urlencode(query)
                # print url
                yield scrapy.Request(
                        url,
                        callback=self.parse
                        )

    def parse(self, response):
        # print response.meta['university']
        univ_name = response.xpath('//span[@class="univ"]/text()').extract()[0]
        url = urlparse.urlparse(response.url)
        query = urlparse.parse_qs(url.query)
        self.logger.info('[%s], page:%d', univ_name, 0)
        yield scrapy.Request(
                response.url,
                callback=self.parse_contents
                )
        # for s in response.xpath('//div[@class="more_result"]/*').extract():
            # print s
        for pageNum in range(len(response.xpath('//div[@class="more_result"]/a').extract())):
            if pageNum == 0: continue
            q = query.copy()
            q['page'] = [pageNum]
            # self.logger.info('[%s], page:%d', univ_name, pageNum)
            u = url._replace(query=urllib.urlencode(q,True))
            self.logger.info('[%s], page:%d', univ_name, pageNum)
            yield scrapy.Request(
                    urlparse.urlunparse(u),
                    callback=self.parse_contents
                    )

    def parse_contents(self, response):
        univ_name = response.xpath('//span[@class="univ"]/text()').extract()[0].strip()
        self.logger.info('[%s] %s', univ_name, response.url)
        for face_cade in response.xpath('//div[@class="face_cade"]'):
            item   = FaceItem()
            pane2  = face_cade.xpath('div[@class="pane2"]')
            # print(face_cade.extract())
            item['name']= pane2.xpath('.//span[@class="name"]/text()').extract()[0].strip()
            keisho  = pane2.xpath('.//span[@class="keisho"]/text()').extract()[0].strip()
            item['gender']      = 'm' if keisho == u"くん" else 'f'
            item['university']  = univ_name
            item['department']  = face_cade.xpath('div[@class="pane1"]//span[@class="course"]/text()').extract()[0].strip()
            face_img_url = pane2.xpath('.//img[@class="face"]/@src').extract()[0]
            item['image_urls'] = [urlparse.urljoin(response.url, face_img_url)]
            # item['image_urls'] = face_img_url
            yield item

