# coding:utf8
import html_downloader
from bs4 import BeautifulSoup
import re

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.csv', 'w')
        format_data = set()


        for data in self.datas:
            for data_ in data:
                fout.write(data_[1].encode('utf-8'))
                fout.write(',')
                fout.write(data_[0])
                fout.write('\n')

                
                #downloader = html_downloader.HtmlDownloader()
                #content = downloader.download(data_)
                #soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
                #table = soup.find('table', id='yw0')
                #tds = table.find_all('td')
                #for td in tds:
                #    fout.write(td.get_text().encode('utf-8'))
                #    fout.write(',')

                #fout.write('\n')

        fout.close()
