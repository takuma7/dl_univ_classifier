# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FaceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def __unicode__(self):
        return repr(self).decode('unicode_escape')

    name = scrapy.Field()
    gender = scrapy.Field()
    university = scrapy.Field()
    department = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

