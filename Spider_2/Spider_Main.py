# coding:utf8

import url_manager
import html_downloader
import html_parser
import html_outputer
import time
import urllib2


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        img_url = 'http://shixin.court.gov.cn/'
        html_cont1 = self.downloader.download(root_url)
        html_cont2 = self.downloader.download(img_url)

        tp1, tp2 = self.parser.parse(root_url, img_url, html_cont1, html_cont2)
        self.outputer.collect_data(tp1)
        self.outputer.collect_data(tp2)

        # get the image:

        self.outputer.output_html()


# main function
if __name__ == "__main__":

    root_url = 'http://shixin.court.gov.cn/index_publish_new.jsp'
    obj_spider = SpiderMain()
    start = time.time()
    obj_spider.craw(root_url)
    end = time.time()
    print '%ds cost.' %(end-start)