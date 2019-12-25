#coding:utf-8
import urllib.request

#网页请求器
class HtmlRequester(object):
    def request(self, url):
        if url is None:
            return None
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:#获取状态码，200表示获取成功
            return None #获取失败
        return response.read()