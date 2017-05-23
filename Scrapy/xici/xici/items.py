# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class XiciItem(Item):
    ip = Field()
    port = Field()
    position = Field()
    type = Field()
    speed = Field()
    last_check_time = Field()
