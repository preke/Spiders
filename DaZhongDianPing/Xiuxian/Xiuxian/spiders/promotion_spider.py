# coding:utf-8
import scrapy
import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse
from scrapy.http import Request
from scrapy.http import Response
from Xiuxian.items import PromotionItem
import re
import requests

class PromotionSpider(scrapy.Spider):
    name = "promotion"
    root = 'http://www.dianping.com'
    start_urls = [
        'http://t.dianping.com/deal/10953643'
    ]

    # def start_requests(self):
    #     url = self.start_urls[self.page]
    #     self.page += 1
    #     print str(self.page) + ' Page'
    #     return [Request(url, callback=self.parse)]

    def parse(self, response):
        temp = response.body
        item = PromotionItem()
        item['_id'] = ''
        str1 = response.url
        for ch in str1:
            try:
                int(ch)
                item['_id'] += ch
            except:
                pass

        soup = BeautifulSoup(temp,from_encoding='utf-8')
        main = soup.find('div', class_='bd')
        title = main.find('h1',class_='title')
        item['name'] = title.get_text().strip()

        sub_title = main.find('h2',class_='sub-title').find('span').get_text()
        item['desc'] = sub_title

        price = main.find('div', class_='price-wrap').find('h3', class_='price').find('span').get_text()
        # print price
        num = float(0)
        for ch in price:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['price'] = num

        action_box = main.find('div', class_='action-box')
        sold = action_box.find('em', class_='J_current_join').get_text()

        num = float(0)
        for ch in sold:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['sold'] = num

        star = action_box.find('span', class_='star-rate').get_text()
        item['stars'] = float(star)

        av_date = main.find('div', class_='validate-date').find('span').get_text()
        item['av_time'] = av_date

        request1 = requests.get(
            'http://t.dianping.com/ajax/detailDealRate',
            params = {
                'dealGroupId': item['_id'],
                'pageNo': 1,
                'filtEmpty': 1,
                'timestamp': 123234534,
            },
            allow_redirects=False
        )

        print request1.headers
        # print soup

        #op_bar = soup.find('div', class_='content').find('div', class_='comment-box J_comment_box').find('div', class_='J_main_comment')#.find('div', class_='op-bar')#.find('div', class_='op-statis Fix')
        #print op_bar