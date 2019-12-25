# coding:utf-8
# Web putper
import os
from  urllib import request
from lxml import etree
import gzip
import datetime

class HtmlOutputer(object):
    def __init__(self):
        self.term_dict = {
            'aircraft': "飞行器",
            'warship': "舰船舰艇",
            'guns': "枪械与单兵",
            'tank': "坦克装甲车辆",
            'artillery': "火炮",
            'missile': "导弹武器",
            'spaceship': "太空装备",
            'explosive': "爆炸物",
        }

    def get_info(self, content, big_cate, second_cate):
        #Get all information according to the maximum value
        data = self.extract_data(content)
        data['大类'] = self.term_dict.get(big_cate)
        data['类型'] = second_cate
        if data:
            print(data)
        return

    def extract_data(self, content):
        title = content[1].replace(' ', '').replace('－', '-').replace('（', '(').replace('）', ')')
        title = title.split('_')
        data = {}
        name = title[0]
        data['名称'] = name
        attrs = content[2:]
        html = content[0]
        selector = etree.HTML(html)
        country = selector.xpath('//span[@class="country"]/b/a/text()')[0]
        image = selector.xpath('//div[@class="maxPic"]/img/@src')
        if not image:
            image = ''
        else:
            image = image[0]
        data['产国'] = country
        data['图片'] = image
        data['简介'] = ''.join(selector.xpath('//div[@class="module"]/p/text()')).replace('\xa0', '').replace('\u3000',
                                                                                                            '').replace(
            '\t', '')
        for attr in attrs:
            if len(attr.split('：')) < 2:
                continue
            key = attr.split('：')[0].replace('（', '(').replace(' ', '').replace('\t', '')
            if key.startswith('(') or len(key) > 6:
                continue
            value = attr.split('：')[1]
            data[key] = value.replace('\t', '').replace('\n', '').replace(',', '')
        return data

    def modify_data(self):#Modify data
        keys = []
        for item in self.conn['military']['kb'].find():
            body = item['contents']
            title = body[1].replace(' ','').replace('－','-').replace('（','(').replace('）',')')
            title = title.split('_')
            data = {}
            name = title[0]
            category = title[1]
            data['名称'] = name
            data['类别'] = category
            attrs = body[2:]
            html = body[0]
            selector = etree.HTML(html)
            country = selector.xpath('//span[@class="country"]/b/a/text()')[0]
            data['产国'] = country
            for attr in attrs:
                if len(attr.split('：')) < 2:
                    continue
                key = attr.split('：')[0].replace('（','(').replace(' ','').replace('\t','')
                if key.startswith('(') or len(key) > 6:
                    continue
                value = attr.split('：')[1]
                data[key] = value.replace('\t','').replace('\n','').replace(',','')
                keys.append(key)
        return
