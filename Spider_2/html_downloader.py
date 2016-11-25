# coding:utf8

import urllib2

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

        req = urllib2.Request(url = url, headers = headers)
        response = urllib2.urlopen(req)
        if response.getcode() != 200:
            return None

        return response.read()
