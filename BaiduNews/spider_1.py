# coding:utf-8
import requests
import hashlib
import urllib2
import urllib
import urlparse
from bs4 import BeautifulSoup

def crawl(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request) 
    html = response.read()
    soup = BeautifulSoup(html, from_encoding='utf-8')
    return soup

def parse(soup, is_homepage):
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
        source_and_time = result.find('p', class_='c-author').get_text()
        source, time = source_and_time.split(u'\xa0'u'\xa0')
        temp_abstract = abstract[len(source_and_time):]
        summary = ""
        for word in temp_abstract:
            summary = summary + word
            if summary[-3:] == '...':
                break
        temp_list = [title, title_url, source, time, summary]
        try:
            simi_words = results[0].find('a', class_='c-more_link').get_text()
            simi_words_url = 'http://news.baidu.com' + results[0].find('a', class_='c-more_link')['href']
            temp_list.append(simi_words)
            temp_list.append(simi_words_url)
            temp = " "
            i = 0
            while i != len(simi_words_url) - 1:
                if simi_words_url[i] == '+':
                    while simi_words_url[i] != '&':
                        temp = temp + simi_words_url[i]
                        i = i + 1
                else:
                    i = i + 1
            temp_list.append(temp)
        except:
            pass
        ans.append(temp_list)

    if is_homepage == 1:
        page_list = []
        try:    
            pages = soup.find('p', id='page').find_all('a')
            for page in pages:
                page_list.append('http://news.baidu.com' + page['href'])
        except:
            pass

        return page_list, ans
    else:
        return ans

def search(query_word):
    word = urllib.quote(query_word)
    url  = 'http://news.baidu.com/ns?cl=2&rn=40&tn=news&word='+word+'&pn=0'
    soup = crawl(url)
    page_list, ans = parse(soup, 1)
    return page_list, ans

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