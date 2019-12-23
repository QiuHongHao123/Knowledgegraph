
from sklearn import svm
from sklearn.externals import joblib
from pyhanlp import *
import tflearn
import numpy as np
from py2neo import Graph
import os


def load_file(filename):
    with open(filename, errors='ignore', encoding='UTF-8') as f:
        x = []
        for line in f:
            line = line.strip('\n')
            line = line.strip('\r')
            line = line.replace(" ", '')
            x.append(line)
    return x


def load_all_file(dirname='./models'):
    x_train = []
    y_train = []
    list = os.listdir(dirname)  # 返回文件夹下文件名字的列表
    print(list)
    for i in range(0, len(list)):
        path = os.path.join(dirname, list[i])
        if os.path.isfile(path):
            x = load_file(path)
            x_train += x
            y = [i] * len(x)
            y_train += y
    return x_train, y_train

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
def creat_model(x_train):
    vp = tflearn.data_utils.VocabularyProcessor(
        max_document_length=100,
        min_frequency=0,
        vocabulary=None,
        tokenizer_fn=chinese_tokenizer
    )
    vp.fit(x_train)
    vp.save('vocab.pickle')

def change_doc_to_vec(x):
    vp=tflearn.data_utils.VocabularyProcessor.restore('vocab.pickle')
    x=vp.transform(x)
    x=np.array(list(x))
    return x

def do_svm():
    x_train,y_train=load_all_file()
    x_train=change_doc_to_vec(x_train)

    clf = svm.SVC(probability=True)
    clf.fit(x_train, y_train)

    pstr=["weapon是哪里制造的?","weapon的射程是多少?","weapon产自哪里?"]
    ptest=[]
    ptest+=pstr
    ptest=change_doc_to_vec(ptest)


    y_pred = clf.predict(ptest)
    joblib.dump(clf, "svm_model.m")                                       #序列化形式保存svm模型
    print(y_pred)

#do_svm()
#x_train,y_train=load_all_file()
#creat_model(x_train)
