# coding:utf-8
import requests
import hashlib
import urllib2
import urllib
import urlparse
from bs4 import BeautifulSoup
import datetime
from urllib import quote
import time

def crawl(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request) 
    html = response.read()
    soup = BeautifulSoup(html, from_encoding='utf-8')
    return soup

def parse(soup):
    results = soup.find('div', id='content_left').find_all('div', class_='result')
    ans = []
    for result in results:
        # title: 新闻标题
        # title_url: 新闻链接
        # source_and_time: 作者/时间
        # source: 作者
        # time: 时间
        # summary: 摘要
        # simi_words: 相同新闻
        # simi_words_url: 相同新闻查询的url
        # simi_words_search: cont:....
        title = result.find('h3', class_='c-title').find('a').get_text()
        title_url = result.find('h3', class_='c-title').find('a')['href']
        try:
            abstract = result.find('div', class_='c-summary c-row ').get_text()
        except:
            abstract = result.find('div', class_='c-span18 c-span-last').get_text()
        try:
            source_and_time = result.find('p', class_='c-author').get_text()
            source, time = source_and_time.split(u'\xa0'u'\xa0')
        except:
            source_and_time = ""
            source = ""
            time = ""
        temp_abstract = abstract[len(source_and_time):]
        summary = ""
        for word in temp_abstract:
            summary = summary + word
            if summary[-3:] == '...':
                break
        temp_list = [title, title_url, source, time, summary]
        temp = " "
        try:
            simi_words = result.find('a', class_='c-more_link').get_text()
            simi_words_url = 'http://news.baidu.com' + result.find('a', class_='c-more_link')['href']
            i = 0
            while i != len(simi_words_url) - 1:
                if simi_words_url[i] == '+':
                    while simi_words_url[i] != '&':
                        temp = temp + simi_words_url[i]
                        i = i + 1
                else:
                    i = i + 1
        except:
            simi_words = ""
            simi_words_url = ""
            temp = ""
        temp_list.append(simi_words)
        temp_list.append(simi_words_url)
        temp_list.append(temp)
        ans.append(temp_list)

#     if is_homepage == 1:
#         page_list = []
#         try:    
#             pages = soup.find('p', id='page').find_all('a')
#             for page in pages:
#                 page_list.append('http://news.baidu.com' + page['href'])
#         except:
#             pass

#         return page_list, ans
#     else:
    return ans

# def search(query_word):
#     word = urllib.quote(query_word)
#     url  = 'http://news.baidu.com/ns?cl=2&tn=news&word=' + word
#     soup = crawl(url)
#     page_list, ans = parse(soup, 1)
#     return page_list, ans

def search(query_word):
    word = urllib.quote(query_word)
    url  = 'http://news.baidu.com/ns?cl=2&tn=news&word=' + word
    return url

def get_more(page_list):
    ans = []
    for page in page_list:
        soup = crawl(page)
        temp_ans = parse(soup, 0)
        ans = ans + temp_ans

    return ans

def get_same(url):
    soup = crawl(url)
    ans = parse(soup, 0)
    return ans

def date_filter(begin_date, end_date, query_word):
    date0 = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    date1 = datetime.datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
    y0, m0, d0 = str(date0.year), str(date0.month), str(date0.day)
    y1, m1, d1 = str(date1.year), str(date1.month), str(date1.day)
    query_word = quote(query_word)
    bt = str(int(time.mktime(date0.timetuple())))
    et = str(int(time.mktime(date1.timetuple())))
    url = 'http://news.baidu.com/ns?from=news&cl=2&bt='+ bt + '&y0='+ y0 +'&m0=' + m0 + '&d0=' + d0 + '&y1=' + y1 + '&m1=' + m1 + '&d1=' + d1 + '&et=' + et + '&q1=' + query_word + '&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date=' + begin_date + '&end_date=' + end_date + '&tn=newsdy&ct1=1&ct=1'
    return url

def page_filter(url, page=0):# append url with pn and rn params
    # rn are set to be 20
    if page is None:
        page = 0
    rn = 20
    pn = page * rn
    rn = str(rn)
    pn = str(pn)
    url = url + '&pn=' + pn
    url = url + '&rn=' + rn
    return url

def search_with_page(query_word, page=0):
    url = search(query_word)
    url = page_filter(url, page)
    return url

def date_filter_with_page(begin_date, end_date, query_word, page=0):
    url = date_filter(begin_date, end_date, query_word)
    url = page_filter(url, page)
    return url