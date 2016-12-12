# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):
    def __init__(self):
        connection=pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db=connection[settings['MONGODB_DB']]
        self.url_collection = db['url']
        self.shop_collection = db['shop']
        self.promotion_collection = db['promotion']
        self.comment_collection = db['comment']
        self.user_collection = db['user']

    def saveOrUpdate(self, collection, item):
        try:
            collection.insert(dict(item))
            return item
        except:
            raise DropItem('重复喽')

    def process_item(self, item, spider):
        if spider.name == 'url':
            self.saveOrUpdate(self.url_collection, item)
        elif spider.name == 'shop':
            self.saveOrUpdate(self.shop_collection, item)
        elif spider.name == 'promotion':
            self.saveOrUpdate(self.promotion_collection, item)
        elif spider.name == 'comment':
            str1 = type(item)
            if str(str1) == "<class 'Xiuxian.items.CommentItem'>":
                self.saveOrUpdate(self.comment_collection, item)
            else:
                self.saveOrUpdate(self.user_collection, item)





# class MySQLPipeline(object):
#     def __init__(self):
#         # MYSQL_HOST = 'localhost'
#         # MYSQL_DBNAME = 'DianPing'
#         # MYSQL_USER = 'debian-sys-maint'
#         # MYSQL_PASSWD = 'V9kflS1yEB4h3bRw'
#         self.connection = MySQLdb.connect(
#             host = settings['MYSQL_HOST'],
#             port = 3306,
#             user = settings['MYSQL_USER'],
#             passwd = settings['MYSQL_PASSWD'],
#             db = settings['MYSQL_DBNAME'],
#         )
#
#
#     def process_item(self, item, spider):
#         cur = self.connection.cursor()
#         insert_url = 'insert into url values(%s, %s)'
#         cur.execute(insert_url, (item['url'], item['id']))
#         cur.close()
#         self.connection.commit()
#         return item


# class XiuxianPipeline(object):
#     def process_item(self, item, spider):
#         return item
