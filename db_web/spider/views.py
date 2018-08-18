from django.shortcuts import render,HttpResponseRedirect
from . import models
from .tools import get_zlzp,get_lgzp,get_qtzp,zl_info,lg_info,qt_info,page



def index(request):
    return render(request,'search.html')

def search_disp(request):
    if request.method!='POST':
        return HttpResponseRedirect('/spider/index')
    else:
        keyword=request.POST.get('keyword')
        website=request.POST.get('website')
        return HttpResponseRedirect('/spider/search/?kw={a}&ws={b}&sl=-1&sh=-1'.format(a=keyword,b=website))


def search(request):
    keyword=request.GET.get('kw')
    website=request.GET.get('ws')
    page_cot=request.GET.get('pn')
    city=request.GET.get('city')
    salaryl=request.GET.get('sl')
    salaryh=request.GET.get('sh')
    city_lst=['北京', '上海', '深圳', '武汉', '西安', '杭州', '南京', '成都', '重庆', '大连', '沈阳', '苏州', '长沙', '合肥', '宁波', '郑州', '天津', '青岛', '济南', '哈尔滨', '长春', '福州']
    if city == None:
        city = '全国'
    if page_cot == None:
        page_cot = 1
    page_lst=page(page_cot)
    if page_cot==1:
        previous=None
    else:
        previous=int(page_cot)-1
    next=int(page_cot)+1
    if website=='zlzp':
        if salaryl=='-1' or salaryh=='-1':
            result=get_zlzp(keyword=keyword,cot=page_cot,city=city)
        else:
            result=get_zlzp(keyword=keyword,cot=page_cot,salaryl=salaryl,salaryh=salaryh,city=city)
        return render(request,'result.html',{'result':result,'keyword':keyword,'city':city,'page_cot':page_cot,'sl':salaryl,'sh':salaryh,'ws':website,'city_lst':city_lst,'page_lst':page_lst
                                             ,'previous':previous,'next':next})

    if website=='lgzp':
        if salaryl=='-1' or salaryh=='-1':
            result=get_lgzp(keyword=keyword,cot=page_cot,city=city)
        else:
            result=get_lgzp(keyword=keyword,cot=page_cot,salaryl=salaryl,salaryh=salaryh,city=city)
        return render(request,'result.html',{'result':result,'keyword':keyword,'city':city,'page_cot':page_cot,'sl':salaryl,'sh':salaryh,'ws':website,'city_lst':city_lst,'page_lst':page_lst
                                            , 'previous': previous, 'next': next})
    if website=='qtzp':
        if salaryl=='-1' or salaryh=='-1':
            result=get_qtzp(keyword=keyword,cot=page_cot,city=city)
        else:
            result=get_qtzp(keyword=keyword,cot=page_cot,salaryl=salaryl,salaryh=salaryh,city=city)
        return render(request,'result.html',{'result':result,'keyword':keyword,'city':city,'page_cot':page_cot,'sl':salaryl,'sh':salaryh,'ws':website,'city_lst':city_lst,'page_lst':page_lst
            , 'previous': previous, 'next': next})


def details(request,website,key):
    print(website)
    print('\n')
    print(key)
    referer=request.META['HTTP_REFERER']
    print(referer)
    key=key.replace('|','/')
    if website=='zlzp':
        result=zl_info(url=key)
        print('开始返回结果')
        return render(request,'jobs_single.html',{'result':result,'referer':referer})
    if website=='qtzp':
        result=qt_info(url=key)
        print('开始返回结果')
        return render(request, 'jobs_single.html', {'result': result,'referer':referer})
    if website=='lgzp':
        result=lg_info(url=key)
        print('开始返回结果')
        return render(request, 'jobs_single.html', {'result': result,'referer':referer})

# def test(request):
#     return render(request,'visualization1.html')