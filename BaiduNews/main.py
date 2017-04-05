# coding:utf-8
import requests
import hashlib
import urllib2
import urlparse
from bs4 import BeautifulSoup
import jieba
from jieba import analyse

def crawl():
    response = urllib2.urlopen('http://mil.news.baidu.com/')  
    html = response.read()
    soup = BeautifulSoup(html, from_encoding='utf-8')
    
    #part 1
    instant_news = soup.find('div', class_='mod').find('div', class_='bd').find_all('li')
    instant_news_list = []
    for li in instant_news:
        instant_news_list.append( (li.find('a')['href'], li.find('a').get_text()) )
    # for element in instant_news_list:
    #     print element[0], element[1]
    
    focal_news = soup.find('div', class_='l-left-col').find('div',class_='b-left').find_all('li')
    focal_news_list = []
    for li in focal_news:
        focal_news_list.append((li.find('a')['href'], li.find('a').get_text()))
    # for element in focal_news_list:
    #     print element[0], element[1]
    
    hot_news = soup.find('div', id='col_guojijq').find('div', class_='l-right-col').find_all('li')
    hot_news_list = []
    for li in hot_news:
        hot_news_list.append((li.find('a')['href'], li.find('a').get_text()))
    # for element in hot_news_list:
    #     print element[0], element[1]

    latest_news = soup.find('div', id='col_latest').find_all('li')
    # instant_news_list = []
    latest_news_list = []
    for li in latest_news:
        temp = (li.find('a')['href'], li.find('a').get_text())
        if temp not in instant_news_list:
            latest_news_list.append(temp)
    
    return instant_news_list, focal_news_list, hot_news_list, latest_news_list

def get_keywords(instant_news_list, focal_news_list, hot_news_list, latest_news_list):
    string = ""
    for s in instant_news_list:
        string = string + s[1]
        string = string + ' '
    for s in focal_news_list:
        string = string + s[1]
        string = string + ' '
    for s in hot_news_list:
        string = string + s[1]
        string = string + ' '
    for s in latest_news_list:
        string = string + s[1]
        string = string + ' '
    
    tags = jieba.analyse.extract_tags(string, 20)
    new_tags = []
    for t in tags:
        try:
            t.decode('utf-8')
        except:
            new_tags.append(t)
    return new_tags[:6]
