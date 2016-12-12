# coding:utf-8
import scrapy
import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse
from scrapy.http import Request
from scrapy.http import Response
from Xiuxian.items import UrlsItem
import re


class UrlSpider(scrapy.Spider):
    name = "url"
    root = 'http://www.dianping.com'
    cnt = 0
    page = 1
    shop_urls = []
    start_urls = [
        'http://www.dianping.com/search/category/4/10'
    ]

    # def start_requests(self):
    #     url = self.start_urls[self.page]
    #     self.page += 1
    #     print str(self.page) + ' Page'
    #     return [Request(url, callback=self.parse)]

    def parse(self, response):
        temp = response.body
        soup = BeautifulSoup(temp,from_encoding='utf-8')
        content = soup.find('div', id='shop-all-list').find_all('li')

        for li in content:
            str = li.find('div', class_='tit').find('a')['href']
            self.shop_urls.append(self.root+ str)

        for url in self.shop_urls:
            item = UrlsItem()

            num = ''
            for ch in url:
                try:
                    int(ch)
                    num += ch
                except:
                    pass

            item['url'] = url
            item['_id'] = num
            yield item

        print 'page: ', self.page
        self.page += 1
        try:
            next_page = soup.find('div', class_ = 'page').find('a', class_ = 'next', title = '下一页')
            url = self.root + next_page['href']
            yield Request(url)
        except:
            pass