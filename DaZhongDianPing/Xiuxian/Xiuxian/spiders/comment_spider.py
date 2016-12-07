# coding:utf-8
import scrapy
import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse
from scrapy.http import Request
from scrapy.http import Response
from Xiuxian.items import CommentItem
from Xiuxian.items import UserItem
import re


class CommentSpider(scrapy.Spider):
    name = "comment"
    root = 'http://www.dianping.com/shop/22987445/review_more'
    cnt = 0
    page = 1
    user_home = 'http://www.dianping.com/member/'
    shop_urls = []
    start_urls = [
        'http://www.dianping.com/shop/22987445/review_more'
    ]

    # def start_requests(self):
    #     url = self.start_urls[self.page]
    #     self.page += 1
    #     print str(self.page) + ' Page'
    #     return [Request(url, callback=self.parse)]

    def __init__(self):
        pass

    def deal_num(self, str):
        ans = ''
        num = 0
        for ch in str:
            try:
                int(ch)
                num *= 10
                num += int(ch)
                break
            except:
                ans += ch

        return [ans, num]


    def user(self, response):
        # print response.url
        temp = response.body
        soup = BeautifulSoup(temp, from_encoding='utf-8')
        item = UserItem()
        str1 = response.url
        id = ''
        for ch in str1:
            try:
                int(ch)
                id += ch
            except:
                pass

        item['_id'] = id

        txt = soup.find('div', class_='txt')
        item['user_name'] = txt.find('h2', class_='name').get_text()
        item['is_vip'] = 0
        try:
            vip = txt.find('div', class_='vip').find('i',class_='icon-vip')
            if vip != None:
                item['is_vip'] = 1
        except:
            pass

        col_exp = txt.find('div', class_='col-exp')
        rank = col_exp.find('span', class_='user-rank-rst')['title']
        num = 0
        for ch in rank:
            try:
                int(ch)
                num *= 10
                num += int(ch)
            except:
                pass

        item['contribution'] = num

        item['gender'] = col_exp.find('span', class_='user-groun').find('i')['class'][0]

        item['city'] = col_exp.find('span', class_='user-groun').get_text()

        try:
            msg = soup.find('div', class_='aside').find('div', class_='user-message').find('ul').find_all('li')[1].get_text()
            item['birthday'] = msg[3:]
        except:
            pass

        yield item





    def parse(self, response):
        print response.url
        temp = response.body
        soup = BeautifulSoup(temp,from_encoding='utf-8')
        try:
            comment_mode = soup.find('div', class_='comment-mode')
            lists = comment_mode.find('div', class_='comment-list').find('ul').find_all('li')
            new_list = []
            for li in lists:
                try:
                    li['data-id']
                    new_list.append(li)
                except:
                    pass

            for li in new_list[:1]:
                item = CommentItem()
                item['_id'] = li['data-id']
                item['user_id'] = li.find('a', class_='J_card')['user-id']

                home = self.user_home + item['user_id']
                yield Request(home, callback=self.user)

                item['user_name'] = li.find('p', class_='name').find('a').get_text().encode('utf-8')
                content = li.find('div', class_='content')
                user_info = content.find('div', class_='user-info')
                stars = user_info.find('span', class_='item-rank-rst')['class']
                tp = self.deal_num(stars[1])
                item['stars'] = tp[1]
                rsts = user_info.find('div', class_='comment-rst').find_all('span', class_='rst')
                tp = self.deal_num(rsts[0].get_text().encode('utf-8'))
                item['label_1'] = dict()
                item['label_1'][tp[0]] = tp[1]

                tp = self.deal_num(rsts[1].get_text().encode('utf-8'))
                item['label_2'] = dict()
                item['label_2'][tp[0]] = tp[1]

                tp = self.deal_num(rsts[2].get_text().encode('utf-8'))
                item['label_3'] = dict()
                item['label_3'][tp[0]] = tp[1]

                item['avg_cost'] = ''
                try:
                    cost = user_info.find('span', class_='comm-per').get_text()
                    num = 0
                    for ch in cost:
                        try:
                            int(ch)
                            num *= 10
                            num += int(ch)
                        except:
                            pass

                    item['avg_cost'] = num
                except:
                    pass

                cont = content.find('div', class_='comment-txt').find('div', class_='J_brief-cont').get_text().strip()
                item['content'] = cont

                item['likes'] = []
                try:
                    dishes = content.find('div', class_='comment-recommend').find_all('a', class_='col-exp')
                    for dish in dishes:
                        item['likes'].append(dish.get_text().encode('utf-8'))

                except:
                    pass


            #     yield item
            #
            # print 'page: ', self.page
            # self.page += 1
            # try:
            #     next_page = soup.find('div', class_ = 'Pages').find('a', class_ = 'NextPage', title = '下一页')
            #     url = self.root + next_page['href']
            #     yield Request(url)
            # except:
            #     pass
        except:
            pass