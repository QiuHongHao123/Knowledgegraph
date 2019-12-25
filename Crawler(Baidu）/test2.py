from baike_spider import url_manager, html_requester, html_parser, html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()# 网页管理器
        self.requester = html_requester.HtmlRequester()# 网页请求器
        self.parser = html_parser.HtmlParser()# 网页解析器
        self.outputer = html_outputer.HtmlOutputer()# 网页输出器

    def craw(self, my_root_url):
        count = 1
        self.urls.add_new_url(my_root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()# 获取待爬取的 URL
                print("craw %d : %s" % (count, new_url))
                html_cont = self.requester.request(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if count == 10:# 爬取 10 条的数据
                    break
                count += 1
            except:
                print("craw failed")

        self.outputer.output_html()


if __name__ == '__main__':
    #入口：URL维基百科的 武器 相关的百度词条
    root_url = "https://baike.baidu.com/item/%E7%AA%81%E5%87%BB%E6%AD%A5%E6%9E%AA/3738226?fr=aladdin"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)# 启动爬虫
