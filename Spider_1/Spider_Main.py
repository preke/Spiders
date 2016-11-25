# coding:utf8

import url_manager
import html_downloader
import html_parser
import html_outputer
import time

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                print 'craw %d' %(count)
                new_url = self.urls.get_new_url()
                html_cont = self.downloader.download(new_url)

                new_urls, new_data = self.parser.parse(new_url, html_cont)
                # add next_page links
                
                if len(new_urls) > 0:
                    self.urls.add_new_urls(new_urls)

                self.outputer.collect_data(new_data)
                count = count + 1
                
            except:
                 print 'failed'

        print 'please wait...'
        self.outputer.output_html()


# main function
if __name__ == "__main__":

    root_url = 'http://www.dailianmeng.com/p2pblacklist/index.html'
    obj_spider = SpiderMain()
    start = time.time()
    obj_spider.craw(root_url)
    end = time.time()
    print '%ds cost.' %(end-start)