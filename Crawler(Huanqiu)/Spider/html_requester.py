#coding:utf-8
import os
from  urllib import request
from lxml import etree
import gzip
import datetime
#网页请求器
class HtmlRequester(object):
    # Web requester
    def get_html(self, url):
        if url is None:
            return None
        headers = {  # Set request header
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_1fc983b4c305d209e7e05d96e713939f=1552034977; Hm_lpvt_1fc983b4c305d209e7e05d96e713939f=1552036141',
            'Host': 'weapon.huanqiu.com'
        }

        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        if response.getcode() != 200:  # Get status code, 200 indicates success
            return None  # Acquisition failure
        page = response.read()
        page = gzip.decompress(page).decode('utf-8')#Specify encoding UTF-8
        return page