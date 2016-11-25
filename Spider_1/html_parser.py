# coding:utf8

from bs4 import BeautifulSoup
import re
import urlparse

class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a',text='后页 >')
        for link in links:
            new_url = link['href']

            new_full_url = urlparse.urljoin(page_url, new_url)
            # print new_full_url
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        new_data = set()
        links = soup.find_all('a', text='查看详情')
        
        for link in links:
            new_url = link['href']
            
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_data.add(new_full_url)

        return new_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8') # what for ?
        new_urls = self._get_new_urls(page_url, soup) # link for nextpage
        new_data = self._get_new_data(page_url, soup) # links of details
        return new_urls, new_data



