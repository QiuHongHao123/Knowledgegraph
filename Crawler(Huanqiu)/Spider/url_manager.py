#coding:utf-8
import os
from  urllib import request
from lxml import etree
import gzip
import datetime


#Web manager
class UrlManager(object):
    def get_maxpage(self, html):  # Get maximum page value
        selector = etree.HTML(html)
        max_pages = selector.xpath('//div[@class="pages"]/a/text()')
        if not max_pages:
            max_page = 1
        else:
            max_page = int(max_pages[-2])

        return max_page





