from django.shortcuts import render
from . import models
import json
import pyspark
from pyspark.sql import HiveContext
from pyspark.sql import SparkSession
from pyspark import SparkContext
from .tools import lable_filter,mon_wa_trans,text_division,desp_text_division,work_exp_trans,new_edu_trans,city_trans,lable_trans,features_trans
from .tools import result_trans
from pyspark.ml.feature import IDFModel,HashingTF
from pyspark.mllib.classification import NaiveBayesModel
from pyspark.sql.types import Row,StructType,StructField,StringType,IntegerType
from pyspark.mllib.linalg import DenseVector
# Create your views here.
def fill_info(request):
    lst_pos=['web','系统工程师','高级软件工程师','软件工程师','软件','软件开发','手机应用','计算机','硬件','数据挖掘','数据库工程师','单片机','嵌入式硬件','嵌入式软件','ios','安卓','android','硬件工程师','系统测试','运维','前端',
             'java开发','高级硬件工程','区块链','大数据','深度学习','人工智能','机器视觉','算法','ui',
              '游戏开发','网络管理','网页设计/制作/美工','软件测试','通信','电子技术','机器人','电气工程师','自动化','电路工程',
              'cocos2d-x','物联网','系统架构','erp实施','电子工程','系统集成','集成电路','硬件测试','数据分析','射频工程','网络安全',
              '半导体','flash']
    lst_exp=['10年以上','5-10年','3-5年','1-3年','无经验']

    return render(request,'fill.html',{'position':lst_pos,'exp':lst_exp})
def salary_pre(request):
    sc=SparkContext('local','test')
    spark = SparkSession.builder.getOrCreate()
    hive_con=HiveContext(sc)
    nd_idf=IDFModel.load('hdfs://localhost:9000/nd_idf_test')
    agg_idf=IDFModel.load('hdfs://localhost:9000/agg_idf_test')
    model=NaiveBayesModel.load(sc,'hdfs://localhost:9000/qtzpnymodel')
    # hive_con.sql('use zp')
    # testdata=hive_con.sql('select education,mon_wa,name,work_area,work_desp,work_exp,work_lable from `qtzp` where id=789')
    # testdataRDD = testdata.rdd.map(lambda i: Row(**{
    #     'education': new_edu_trans(i.education),
    #     'salary': mon_wa_trans(i.mon_wa),
    #     'name': i.name,
    #     'city': i.work_area,
    #     'work_desp': i.work_desp,
    #     'work_exp': i.work_exp,
    #     'work_lable': i.work_lable
    # }))
    # dataDF=testdataRDD.map(lambda i:Row(**{
    #     'salary': int(i.salary),
    #     'agg': [i.education] + [i.city] + [i.work_lable] + [i.work_exp],
    #     'name_and_desp': desp_text_division(i.name + ',' + i.work_desp)
    # })).toDF()
    # dataDF.show()
    city=request.POST.get('city')
    edu=request.POST.get('education')
    introduce=request.POST.get('introduce')
    position=request.POST.get('job')
    exp=request.POST.get('exp')
    dataRDD=sc.parallelize([[edu,city,position,exp,introduce]])
    schema=StructType([StructField('education',StringType(),True),StructField('work_area',StringType(),True),StructField('work_lable',
            StringType(),True),StructField('work_exp',StringType(),True),StructField('work_desp',StringType(),True)])
    rowRDD=dataRDD.map(lambda i:Row(i[0],i[1],i[2],i[3],i[4]))
    dataDF=spark.createDataFrame(rowRDD,schema)
    dataDF.show()
    dataDF=dataRDD.map(lambda i:Row(**{
        'education':i[0],
        'work_area':i[1],
        'work_lable':i[2],
        'work_exp':i[3],
        'work_desp':i[4]
    })).map(lambda i:Row(**{
        'education':str(new_edu_trans(i.education)),
        'city':[i.work_area],
        'work_desp':i.work_desp,
        'work_lable':[i.work_lable],
        'work_exp':[i.work_exp]
    })).map(lambda i:Row(**{
        'agg':[i.education] + i.city + i.work_lable + i.work_exp,
        'name_and_desp':desp_text_division(i.work_desp)
    })).toDF()
    dataDF.show()

    ndtf = HashingTF(inputCol='name_and_desp', outputCol='ndFeatures', numFeatures=10240)
    aggtf = HashingTF(inputCol='agg', outputCol='Features_agg', numFeatures=256)
    data = ndtf.transform(dataDF)
    data = aggtf.transform(data)
    idfdata = nd_idf.transform(data)
    idfdata = agg_idf.transform(idfdata)
    RDD = idfdata.rdd
    # featuresRDD = RDD.map(lambda i: (i.salary, i.ndfeatures.toArray().tolist() + i.features_agg.toArray().tolist()))  #test
    featuresRDD = RDD.map(lambda i: i.ndfeatures.toArray().tolist() + i.features_agg.toArray().tolist())      #应用
    # featuresRDD = featuresRDD.map(lambda i: features_trans(i))      #test
    featuresRDD=featuresRDD.map(lambda i:DenseVector(i))       #应用
    # result=featuresRDD.map(lambda i: model.predict(i.features)).collect()       #test
    result=featuresRDD.map(lambda i:model.predict(i)).collect()
    # result=result[0]
    sc.stop()
    city_mean=models.CSR.objects.using('db2').filter(city__contains=city)
    city_mean=city_mean[0].salary
    salary=result_trans(result[0])
    pos_mean=models.ITS.objects.using('db2').get(name=position)
    pos_mean=pos_mean.salary
    data_lst=[city_mean,pos_mean,salary]
    data_lst=json.dumps(data_lst)
    return render(request,'salary.html',{'result':result,'position':position,'city':city,'edu':edu,'exp':exp,'data':data_lst})


def vt(request):
    leibie=request.GET.get('lb')
    if leibie==None:
        data=models.BDT.objects.using('db2').all()
        name_lst=[]
        lst=[]
        for i in data:
            dct={}
            dct['value']=i.count
            dct['name']=i.name
            print(dct)
            lst.append(dct)
        for i in lst:
            name_lst.append(i['name'])
        print(name_lst)
        lst=json.dumps(lst[1:])
        name_lst=json.dumps(name_lst[1:])
        return render(request,'visualization.html',{'data':lst,'name':name_lst})
    if leibie=='1':
        city_lst=[]
        sal_lst=[]
        data=models.CSR.objects.using('db2').all()
        data=data[:10]
        for i in data:
            city_lst.append(i.city)
            sal_lst.append(i.salary)
        city_lst=json.dumps(city_lst)
        sal_lst=json.dumps(sal_lst)
        print(city_lst)
        print(sal_lst)
        return render(request,'visualization1.html',{'city':city_lst,'salary':sal_lst})
    if leibie=='2':
        lst=[]
        itc_data=models.ITC.objects.using('db2').all()
        its_data=models.ITS.objects.using('db2').all()
        name_lst=[]
        for i in itc_data:      #完成职位lst
            name_lst.append(str(i))
        for i in name_lst:
            tem_lst=[]
            tem_lst.append(int(itc_data.get(name=i).count))
            tem_lst.append(int(its_data.get(name=i).salary))
            tem_lst.append(i)
            lst.append(tem_lst)
        lst=json.dumps(lst)
        print(lst)
        return render(request,'visualization2.html',{'data':lst})
    if leibie=='3':
        lst=[]
        data=models.BPS.objects.using('db2').all()
        for i in data:
            tem_lst=[]
            tem_lst.append(i.count)
            tem_lst.append(i.salary)
            tem_lst.append(i.name)
            lst.append(tem_lst)
        lst=json.dumps(lst)
        return render(request,'visualization3.html',{'data':lst})
    if leibie=='4':
        lst=[]
        data=models.BDC.objects.using('db2').filter(count__gte=10)
        for i in data:
            tem_lst=[]
            tem_lst.append(i.count)
            tem_lst.append(i.salary)
            tem_lst.append(i.name)
            lst.append(tem_lst)
        lst=json.dumps(lst)
        return render(request,'visualization4.html',{'data':lst})

def processing(request):
    return render(request,'processing1.html')
