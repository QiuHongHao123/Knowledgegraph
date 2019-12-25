#coding:utf-8
import os
from  urllib import request
from lxml import etree
import gzip
import datetime
# Web parser

class HtmlParser(object):
    def get_urllist(self, html):
        #html = self.requester.get_html(url)
        selector = etree.HTML(html)
        links = selector.xpath('//li/span[@class="pic"]/a/@href')  # Find the link labeled ‘a’ under the class ‘pic’
        papers = ['http://weapon.huanqiu.com' + i for i in
                  links]  # The link obtained is incomplete, and the URL needs to be spliced
        return list(set(papers))

    def html_parser(self, html):
        #html = self.requester.get_html(url)
        selector = etree.HTML(html)
        title = selector.xpath('//title/text()')[0]  # Get title
        attrs = selector.xpath('//div[@class="dataInfo"]/ul/li')  # Get content
        contents = [html, title]
        for article in attrs:
            content = article.xpath('string(.)')
            contents.append(content)
        return contents
