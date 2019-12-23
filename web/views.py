from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
from NLP import do_qa
from NLP.creat_classify_model import  chinese_tokenizer


# Create your views here.


def index(request):
    return render(request, "index.html")


def search(request):
    if request.method == 'POST':
        msgInput = request.POST.get("msg_input", None)
        print(msgInput)
        answer = do_qa.do.get_answers(msgInput)
        print(answer)
        return render(request, "index.html",{"data":answer})




'''
def index(request):#request是必须带的实例。类似class下方法必须带self一样
    
    # request.POST
    # request.GET
    # return HttpResponse("Hello World!!")#通过HttpResponse模块直接返回python 字符串到前端页面
    return render(request,"index.html")
'''