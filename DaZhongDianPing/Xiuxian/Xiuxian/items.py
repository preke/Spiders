# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UrlsItem(scrapy.Item):
    url = scrapy.Field()
    _id = scrapy.Field()

class ShopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()
    addr = scrapy.Field()
    time = scrapy.Field()
    first_category = scrapy.Field()
    district = scrapy.Field()
    second_category = scrapy.Field()
    stars = scrapy.Field()
    num_of_comment = scrapy.Field()
    avg_cost = scrapy.Field()
    label_1 = scrapy.Field()
    label_2 = scrapy.Field()
    label_3 = scrapy.Field()
    prom = scrapy.Field()
    # update_time = scrapy.Field()

class PromotionItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    sold = scrapy.Field()
    stars = scrapy.Field()
    av_time = scrapy.Field()
    num_of_comment = scrapy.Field()
    one_star = scrapy.Field()
    two_star = scrapy.Field()
    three_star = scrapy.Field()
    four_star = scrapy.Field()
    five_star = scrapy.Field()



class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
