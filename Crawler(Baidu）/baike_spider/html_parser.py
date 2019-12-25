#coding:utf-8
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from urllib.parse import urljoin
import urllib.parse
#网页解析器

class HtmlParser(object):

    #获取新url函数
    def _get_new_urls(self, page_url, soup):

        new_urls = set()
        # <a target="_blank" href="/view/845405.htm">Unix shell</a>
        links = soup.find_all('a', href=re.compile(r"/item/"))#查找标签为a的开头为/item/的内容
        for link in links:
            new_url = link['href']#获取链接
            new_full_url = urllib.parse.urljoin(page_url, new_url)#获得的的链接不全，需要拼接 url
            new_urls.add(new_full_url)#得到新的链接
        return new_urls

    # 获取内容函数
    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url'] = page_url
        #  <dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find("h1")
        res_data['title'] = title_node.get_text()# 获取标题
        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()#获取简介
        return res_data

    def parse(self, page_url, html_content):
        if page_url is None or html_content is None:
            return
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')#创建BeautifulSoup对象，指定编码utf-8
        new_urls = self._get_new_urls(page_url, soup)#调用获取新url函数
        new_data = self._get_new_data(page_url, soup)#调用获取内容函数

        return new_urls, new_data
