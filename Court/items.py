# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LawyerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    office = scrapy.Field()
    phone = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()


class ZoneItem(scrapy.Item):
    # province = scrapy.Field()
    city = scrapy.Field()