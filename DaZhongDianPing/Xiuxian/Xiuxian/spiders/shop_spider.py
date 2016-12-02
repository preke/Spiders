# coding:utf-8
import scrapy
import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse
from scrapy.http import Request
from scrapy.http import Response
# from Xiuxian.items import urlsItem
import re
import MySQLdb
from scrapy.conf import settings


class ShopSpider(scrapy.Spider):
    name = "shop"
    root = 'http://www.dianping.com'
    connection = MySQLdb.connect(
        host=settings['MYSQL_HOST'],
        port=3306,
        user=settings['MYSQL_USER'],
        passwd=settings['MYSQL_PASSWD'],
        db=settings['MYSQL_DBNAME'],
    )
    start_urls = ['http://www.dianping.com/shop/5250506']

    # def __init__(self):
    #     cur = self.connection.cursor()
    #     cnt = cur.execute('select url from url where 1=1')
    #     urls = cur.fetchmany(cnt)
    #     for url in urls:
    #         self.start_urls.append(url[0])
    #     cur.close()
    #     self.connection.close()


    def parse(self, response):
        temp = response.body
        soup = BeautifulSoup(temp, from_encoding='utf-8')
        pass