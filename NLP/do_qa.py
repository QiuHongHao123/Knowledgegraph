from py2neo import Graph,Node,Relationship
from sklearn.externals import joblib
from NLP.creat_classify_model import chinese_tokenizer
import tflearn
import numpy as np
from pyhanlp import *
from web import views



def chinese_tokenizer(documents):
    """
    把中文文本转为词序列
    """
    CRFnewSegment = HanLP.newSegment("crf")
    for document in documents:
        words=[]
        # 分词
        seged=CRFnewSegment.seg(document)
        for s in seged:
            words.append(s.word)
        yield words
class do_qa():
    CRFnewSegment = HanLP.newSegment("crf")
    graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    search_sql=[
        "match (n:Weapon{name:'rweapon'}) return n.射程",
        "match (w{name:'rweapon'})-[:`产国`]-(n) return n.name",
        "match (n:Weapon{name:'rweapon'}) return n.乘员",
        "match (a)-[r:研发单位]->(x) where a.name='rweapon' return x.name",
        "match (a)-[r:制造单位]->(x) where a.name='rweapon' return x.name",
        "match (a)-[r:位于]->(x) where a.name='rorgan' return x.name",

    ]

    def classify(self,question):

        have_seg = self.CRFnewSegment.seg(question)
        question = question.replace(" ", '')
        for i in have_seg:
            if i.nature.toString() == 'weapon':
                question=question.replace(i.word,'weapon')
            if i.nature.toString() == 'nation':
                question = question.replace(i.word, 'nation')
            if i.nature.toString() == 'label':
                question = question.replace(i.word, 'label')
            if i.nature.toString() == 'ni':
                question = question.replace(i.word, 'organ')

        toclassify=[]
        toclassify.append(question)
        vp = tflearn.data_utils.VocabularyProcessor.restore('F:/PyCharm/Demo/NLP/vocab.pickle')  # 加载词汇表模型
        toclassify = vp.transform(toclassify)
        toclassify = np.array(list(toclassify))
        clf = joblib.load("F:/PyCharm/Demo/NLP/svm_model.m")
        classify=clf.predict(toclassify )
        #print(classify)
        return classify[0]
    def get_answers(self,question):
        classify_result=self.classify(question)
        print("类别为：",classify_result)
        output=[]
        if classify_result==0:
            output=self.answer_0(question)
        if classify_result == 1:
            output =self.answer_1(question)
        if classify_result == 2:
            output =self.answer_2(question)
        if classify_result==3:
            output =self.answer_3(question)
        if classify_result == 4:
            output =self.answer_4(question)
        if classify_result == 5:
            output =self.answer_5(question)
        if classify_result==6:
            output =self.answer_6(question)
        return output



    def answer_0(self,question):
        have_seg = self.CRFnewSegment.seg(question)
        weapon=""
        for i in have_seg:
            if i.nature.toString() == 'weapon':
                print(i.word)
                weapon=i.word
        sql=self.search_sql[0].replace('rweapon',weapon)
        print(sql)
        answers=self.graph.run(sql).data()
        print(answers)
        out_put=[]
        for i in answers:
            out_put.append(i.get('n.射程'))
            #print(i.get('n.射程'))
        return out_put

    def answer_1(self, question):
        have_seg = self.CRFnewSegment.seg(question)
        weapon = ""
        out_put = []
        for i in have_seg:
            if i.nature.toString() == 'weapon':
                print(i.word)
                weapon = i.word
        sql = self.search_sql[1].replace('rweapon', weapon)

        print(sql)
        answers = self.graph.run(sql).data()
        for i in answers:
            #print(i.get('n.name'))
            out_put.append(i.get('n.name'))
        return out_put

    def answer_2(self,question):
        have_seg = self.CRFnewSegment.seg(question)
        weapon = ""
        output=[]
        for i in have_seg:
            if i.nature.toString() == 'weapon':
                print(i.word)
                weapon = i.word
        sql = self.search_sql[2].replace('rweapon', weapon)
        print(sql)
        answers = self.graph.run(sql).data()
        for i in answers:
            #print(i.get('n.乘员'))
            output.append(i.get('n.乘员'))
        return output

    def answer_3(self,question):
        have_seg = self.CRFnewSegment.seg(question)
        weapon = ""
        output=[]
        for i in have_seg:
            if i.nature.toString() == 'weapon':
                print(i.word)
                weapon = i.word
        sql = self.search_sql[3].replace('rweapon', weapon)
        print(sql)
        answers = self.graph.run(sql).data()
        for i in answers:
            #print(i.get('x.name'))
            output.append(i.get('x.name'))
        return output
    def answer_4(self,question):
        have_seg = self.CRFnewSegment.seg(question)
        weapon = ""
        output=[]
        for i in have_seg:
            if i.nature.toString() == 'weapon':
                print(i.word)
                weapon = i.word
        sql = self.search_sql[4].replace('rweapon', weapon)
        print(sql)
        answers = self.graph.run(sql).data()
        for i in answers:
           #print(i.get('x.name'))
           output.append(i.get('x.name'))
        return output

    def answer_5(self,question):
        have_seg = self.CRFnewSegment.seg(question)
        rorgan = ""
        output=[]
        for i in have_seg:
            if i.nature.toString() == 'ni':
                print(i.word)
                rorgan = i.word
        sql = self.search_sql[5].replace('rorgan', rorgan)
        print(sql)
        answers = self.graph.run(sql).data()
        for i in answers:
            #print(i.get('x.name'))
            output.append(i.get('x.name'))
        return output


do=do_qa()
'''
output1=do.get_answers("四式203毫米重火箭是哪个国家生产的")
output2=do.get_answers("四式203毫米重火箭能射多远")
output3=do.get_answers("苏-27战斗机能载多少人")
output4=do.get_answers("寇蒂斯公司在哪儿")
output5=do.get_answers("四式203毫米重火箭能射多少距离")
for i in output1:
    print(i)
for i in output2:
    print(i)
for i in output3:
    print(i)
for i in output4:
    print(i)
for i in output5:
    print(i)
'''
