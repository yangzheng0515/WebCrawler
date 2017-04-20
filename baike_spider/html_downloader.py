# -*- coding: UTF-8 -*-
import urllib.request

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            return None
        html_cont = response.read().decode('utf-8')
        return html_cont    
