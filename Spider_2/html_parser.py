# coding:utf8

from bs4 import BeautifulSoup
import re
import urlparse
import urllib2
import urllib
from PIL import Image
from pytesser import *
import pytesseract


class HtmlParser(object):
    def get_names(self, page_url, soup):
        tp1 = set()
        links = soup.find('div', id='div1').find_all('a', class_ = 'View')
        #table = soup

        for link in links:
            name = link.get_text().strip()
            id = link.find_parent().find_next_sibling().get_text()
            tp1.add((id, name))

        tp2 = set()
        links = soup.find('div', id='div2').find_all('a', class_='View')
        # table = soup

        for link in links:
            name = link.get_text().strip()
            id = link.find_parent().find_next_sibling().get_text()
            tp2.add((id, name))

        return tp1, tp2

    def get_image(self, img_url, soup):
        pass
        #img = soup.find('img')
        #print str(img)
        #src = urlparse.urljoin(img_url, img['src'])
        #print src
        #path = '1.jsp'
        #headers = {
        #    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        #req = urllib2.Request(url=src, headers=headers)
        #img = urllib2.urlopen(req).read()
        #x = 1
        #urllib.urlretrieve(src, '%s.jsp' % x)

        # img.read().show()

        # vcode = pytesseract.image_to_string(img)
        # print vcode
        #im = Image.open(img)
        # img.show()
        # return img

    def parse(self, name_url, img_url, html_cont1, html_cont2):
        if img_url is None or html_cont1 is None or name_url is None or html_cont2 is None:
            return

        soup1 = BeautifulSoup(html_cont1, 'html.parser', from_encoding='utf-8')  # what for ?
        # soup2 = BeautifulSoup(html_cont2, 'html.parser', from_encoding='utf-8')  # what for ?
        tp1, tp2 = self.get_names(name_url, soup1) # links of details
        #img = self.get_image(img_url, soup2)
        return tp1, tp2



