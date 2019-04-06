# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    city = scrapy.Field()
    district = scrapy.Field()
    job_salary = scrapy.Field()
    company = scrapy.Field()
    title = scrapy.Field()
    edu = scrapy.Field()
    exp = scrapy.Field()
    come_from = scrapy.Field()
