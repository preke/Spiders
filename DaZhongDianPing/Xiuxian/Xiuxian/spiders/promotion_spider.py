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
import pymongo
from scrapy.conf import settings

class PromotionSpider(scrapy.Spider):
    name = "promotion"
    root = 'http://www.dianping.com'
    start_urls = []
    urls = []
    item = PromotionItem()
    cnt = -1
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        sets = db['shop'].find({})
        connection.close()
        urls = []
        for elem in sets:
            try:
                elem['prom']
                for url in elem['prom']:
                    if url[:27] == 'http://t.dianping.com/deal/':
                        urls.append(url)
            except:
                pass

        # for url in urls:
        #     print url
        # print len(urls)
        urls = list(set(urls))

        self.start_urls.append(urls[0])
        self.urls = urls[1:]

    def find(self, s1, s2):
        for ch in s1:
            if ch == s2:
                return True

        return False

    def make_up_ajax(self, s1, id):
        #'http://t.dianping.com/ajax/detailDealRate?dealGroupId=10953643&pageNo=1&filtEmpty=1&timestamp=123123123'
        ans = 'http://t.dianping.com/ajax/detailDealRate?dealGroupId='
        ans += id
        ans += '&pageNo=1&filtEmpty=1&timestamp=123123123'
        return ans



    def get_ajax(self, response):
        temp = response.body
        soup = BeautifulSoup(temp, from_encoding='utf-8')
        try:
            self.item['num_of_comment'] = int(soup.find('p', class_='c-num').find('b').get_text())
            fig = soup.find('div', class_='op-statis Fix').find('div', class_='fig-show').find_all('p', class_='list')
            # print len(fig)
            self.item['five_star'] = int(fig[0].find('span', class_='n-bg J_fig')['data'])
            self.item['four_star'] = int(fig[1].find('span', class_='n-bg J_fig')['data'])
            self.item['three_star'] = int(fig[2].find('span', class_='n-bg J_fig')['data'])
            self.item['two_star'] = int(fig[3].find('span', class_='n-bg J_fig')['data'])
            self.item['one_star'] = int(fig[4].find('span', class_='n-bg J_fig')['data'])
        except:
            self.item['num_of_comment'] = ''
            self.item['five_star'] = ''
            self.item['four_star'] = ''
            self.item['three_star'] = ''
            self.item['two_star'] = ''
            self.item['one_star'] = ''

        yield self.item
        self.item = PromotionItem()
        print self.urls[self.cnt+1]
        self.cnt += 1
        try:
            yield Request(self.urls[self.cnt])
        except:
            pass

    def parse(self, response):
            s1 = response.url
            self.item['_id'] = ''
            for ch in s1:
                try:
                    int(ch)
                    self.item['_id'] += ch
                except:
                    pass

            temp = response.body
            soup = BeautifulSoup(temp, from_encoding='utf-8')
            main = soup.find('div', class_='bd')
            title = main.find('h1', class_='title')
            self.item['name'] = title.get_text().strip()

            sub_title = main.find('h2', class_='sub-title').find('span').get_text()
            self.item['desc'] = sub_title

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

            self.item['price'] = num

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

            self.item['sold'] = num

            try:
                star = action_box.find('span', class_='star-rate').get_text()
                self.item['stars'] = float(star)
            except:
                self.item['stars'] = ''

            av_date = main.find('div', class_='validate-date').find('span').get_text()
            self.item['av_time'] = av_date



            url_temp = self.make_up_ajax(s1, self.item['_id'])
            yield Request(url_temp, callback=self.get_ajax)
