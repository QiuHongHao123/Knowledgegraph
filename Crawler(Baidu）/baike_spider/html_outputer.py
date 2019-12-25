# coding:utf-8
# 网页输出器


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        # 以txt形式进行输出
        count=1
        fout = open("output.txt", "w", encoding='utf-8') # 确定编码格式utf-8
        fout.write("Crawl Results\n")
        for data in self.datas:
            fout.write(str(count)+".%s\n" % (data["title"]))
            fout.write("%s\n" % data["summary"])
            fout.write("上一层：\n")
            count+=1
        # 关闭输出器
        fout.close()
