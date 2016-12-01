# coding:utf-8
import scrapy
import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse
from scrapy.http import Request
from scrapy.http import Response
from Xiuxian.items import urlItem
import re


class FunSpider(scrapy.Spider):
    name = "fun"
    root = 'http://www.dianping.com'
    shop_urls = []
    start_urls = [
        'http://www.dianping.com/search/category/4/30'
    ]

    def parse(self, response):
        temp = response.body
        soup = BeautifulSoup(temp,from_encoding='utf-8')
        content = soup.find('div', id='shop-all-list').find_all('li')

        for li in content:
            str = li.find('div', class_='tit').find('a')['href']
            self.shop_urls.append(self.root+ str)

        # for url in self.shop_urls:
        #     item = urlItem()
        #     item['url'] = url
        #     item['id'] =

        try:
            next_page = soup.find('div', class_ = 'page').find('a', class_ = 'next', title = '下一页')
            url = self.root + next_page['href']

            return [Request(url)]
        except:
            pass