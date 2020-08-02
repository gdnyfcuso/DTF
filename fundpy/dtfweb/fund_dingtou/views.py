from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')
def add(args):
    return HttpResponse("添加数据成功")
def funddata(request):
    fundlist='001,002,003'
    return HttpResponse(fundlist)
        
    