# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaLinkItem(scrapy.Item):
    image = scrapy.Field()
    href = scrapy.Field()


class SinaItem(scrapy.Item):
    id = scrapy.Field()
    valid = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    href = scrapy.Field()
    channel = scrapy.Field()
    tags = scrapy.Field()
