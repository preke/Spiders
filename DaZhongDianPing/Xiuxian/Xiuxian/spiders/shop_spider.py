# coding:utf-8
import scrapy
import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse
from scrapy.http import Request
from scrapy.http import Response
from Xiuxian.items import ShopItem
import re
import pymongo
from scrapy.conf import settings


class ShopSpider(scrapy.Spider):
    name = "shop"
    root = 'http://www.dianping.com'
    start_urls = []
    urls = []
    cnt = -1
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db=connection[settings['MONGODB_DB']]
        set = db['url'].find({})
        connection.close()
        urls = []
        for elem in set:
            urls.append(elem['url'])

        self.start_urls.append(urls[0])
        self.urls = urls[1:]


    def deal_label(self, str):
        ans = ''
        num = 0
        for ch in str:
            if ch != '(' and ch != ')':
                try:
                    int(ch)
                    num *= 10
                    num += int(ch)
                except:
                    ans += ch

        return [ans, num]

    def parse(self, response):
        temp = response.body
        soup = BeautifulSoup(temp, from_encoding='utf-8')
        # print soup
        content = soup.find('div', id='basic-info')
        # print content
        item = ShopItem()

        name = content.find('h1', class_='shop-name').get_text().strip()
        temp = ""
        for ch in name:
            if ch == '\n':
                break
            else:
                temp += ch

        item['name'] = temp.encode('utf-8')

        tel = content.find('p', class_='expand-info tel')
        tel_spans = tel.find_all('span', class_='item', itemprop='tel')
        item['tel'] = []
        for span in tel_spans:
            item['tel'].append(span.get_text().encode('utf-8'))


        div_addr = content.find('div', class_='expand-info address')
        span_addr = div_addr.find('span', class_='item')
        item['addr'] = span_addr['title'].encode('utf-8')

        div_other = content.find('div', class_='other')
        time = div_other.find('p', class_='info info-indent').find('span', class_='item').get_text()
        item['time'] = time.encode('utf-8').strip()

        breadcrumb = soup.find('div', class_='breadcrumb')
        cates = breadcrumb.find_all('a')
        item['first_category'] = cates[0].get_text().strip()
        item['district'] = cates[1].get_text().strip()
        item['second_category'] = cates[2].get_text().strip()

        brief_info = content.find('div', class_='brief-info')
        spans = brief_info.find_all('span')
        str1 = spans[0]['class'][1]
        num = 0
        for ch in str1:
            try:
                num *= 10
                num += int(ch)
            except:
                pass

        num = float(num)
        item['stars'] = float(num/10)

        str1 = spans[1].get_text()
        num = 0
        for ch in str1:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['num_of_comment'] = num

        str1 = spans[2].get_text()
        num = 0
        for ch in str1:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['avg_cost'] = num

        str1 = spans[3].get_text()
        tag = str1[:2]
        num = float(0)
        for ch in str1:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['label_1'] = (tag, num/10)

        str1 = spans[4].get_text()
        tag = str1[:2]
        num = float(0)
        for ch in str1:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['label_2'] = (tag, num/10)

        str1 = spans[5].get_text()
        tag = str1[:2]
        num = float(0)
        for ch in str1:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['label_3'] = (tag, num/10)

        item['_id'] =''
        str1 = response.url
        for ch in str1:
            try:
                int(ch)
                item['_id'] +=ch
            except:
                pass

        prom = []
        try:
            sales = soup.find('div', id='sales')
            links = sales.find_all('a')
            for link in links:
                try:
                    if link['href'] !='javascript:;':
                        prom.append(link['href'])
                except:
                    pass
        except:
            pass

        item['prom'] = prom

        item['labels'] = dict()
        try:
            labels = soup.find('div', id='comment').find('div', class_='J-comment-condition').find_all('span', class_='J-summary')
            # print labels
            for label in labels:
                ans = self.deal_label(label.get_text())
                # print ans[0].encode('utf-8')
                item['labels'][ ans[0].encode('utf-8')] = ans[1]
                # print item['labels']
        except:
            pass

        yield item

        print self.urls[self.cnt+1]
        self.cnt += 1
        try:
            yield Request(self.urls[self.cnt])
        except:
            pass


