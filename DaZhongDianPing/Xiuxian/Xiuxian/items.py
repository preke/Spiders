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
    labels = scrapy.Field()

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
    _id = scrapy.Field()
    shop_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    stars = scrapy.Field()
    label_1 = scrapy.Field()
    label_2 = scrapy.Field()
    label_3 = scrapy.Field()
    content = scrapy.Field()
    avg_cost = scrapy.Field()
    likes = scrapy.Field()


class UserItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    is_vip = scrapy.Field()
    contribution = scrapy.Field()
    birthday = scrapy.Field()
    city = scrapy.Field()
    gender = scrapy.Field()
