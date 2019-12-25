#coding = utf-8
import os
from  urllib import request
from lxml import etree
import gzip
import datetime
from Spider import url_manager, html_requester, html_parser, html_outputer

class NewspaperSpider:
    def __init__(self):

        self.urls = url_manager.UrlManager()  # 网页管理器
        self.requester = html_requester.HtmlRequester()  # 网页请求器
        self.parser = html_parser.HtmlParser()  # 网页解析器
        self.outputer = html_outputer.HtmlOutputer()  # 网页输出器
        return


    #Crawler scheduler
    def spider_main(self):
        big_cates = ['aircraft', 'warship',
                     'guns', 'tank',
                     'artillery', 'missile',
                     'spaceship', 'explosive'
                     ]
        for big_cate in big_cates:
            # Entrance:：url of “weapon” in Huanqiu Military
            big_url = 'http://weapon.huanqiu.com/weaponlist/%s'%big_cate
            html = self.requester.get_html(big_url)
            selector = etree.HTML(html)
            span = selector.xpath('//span[@class="list"]')[0]
            second_urls = ['http://weapon.huanqiu.com' + i for i in span.xpath('./a/@href')]
            second_cates = [i for i in span.xpath('./a/text()')]
            second_dict = {}
            for indx, second_cate in enumerate(second_cates):
                second_dict[second_cate] = second_urls[indx]
            for second_cate, second_url in second_dict.items():
                html = self.requester.get_html(second_url)
                max_pages = self.urls.get_maxpage(html)
                for page in range(1, max_pages+1):
                    url = second_url + '_0_0_%s'%page
                    html = self.requester.get_html(url)
                    seed_urls = self.parser.get_urllist(html)
                    for seed in seed_urls:
                        html = self.requester.get_html(seed)
                        content = self.parser.html_parser(html)
                        self.outputer.get_info(content, big_cate, second_cate)


if __name__ == '__main__':
    handler = NewspaperSpider()
    handler.spider_main()#Start crawler