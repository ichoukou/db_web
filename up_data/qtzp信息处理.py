from pyspark.sql import HiveContext
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import Row,StructField,StringType,StructType,IntegerType,ArrayType,FloatType
from .tools import lable_filter,mon_wa_trans,text_division,desp_text_division,work_exp_trans,new_edu_trans,city_trans,lable_trans,features_trans
from .tools import bigdt,bigdt_lable,bigdt_pp
from pyspark.ml.feature import IDF,HashingTF,IDFModel
from pyspark.mllib.classification import NaiveBayes,NaiveBayesModel
from .tools import test
import sqlalchemy
from sqlalchemy import Column,create_engine,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
class QtzpHanld(object):
    def __init__(self,user='root',password='19985247',dbname='zp',host='127.0.0.1'):
        self.sc=SparkContext('local','test')
        self.hive_con=HiveContext(self.sc)
        self.spark=SparkSession.builder.getOrCreate()
        self.engine=create_engine('mysql+mysqlconnector://{u}:{passwd}@{ip}:3306/{db}'.format(u=user,passwd=password,db=dbname,ip=host))
        self.DBsession=sessionmaker(bind=self.engine)

    def create_table(self):
        from models import Base
        # PSrank, CSrank, BCrank, BTrank, ITCrank, BPSrank, BPrank, BCSrank,
        Base.metadata.create_all(self.engine)

    def salary_top10(self):
        from models import PSrank,CSrank,ITCrank,BCSrank,BPSrank,BDTrank
        #职位分类工资top10
        session=self.DBsession()
        self.hive_con.sql('use zp')
        data=self.hive_con.sql('select work_lable,mon_wa from zp').toDF('work_lable','mon_wa')
        data=data.filter(data['work_lable']!='').rdd
        data_df=self.spark.createDataFrame(data.map(lambda i:[lable_filter(i.work_lable),int(i.mon_wa)]))\
            .toDF('work_lable','salary')
        data_df.groupBy('work_lable').mean().createTempView('salary_sort')
        cot=1
        for i in self.spark.sql('select * from salary_sort order by `avg(salary)` desc').collect():
            if str(i[0])=='1':
                continue
            ps=PSrank()
            ps.id=cot
            ps.name=i[0]
            ps.salary=float(i[1])
            session.add(ps)
            cot+=1
            session.commit()
            print(i)

        #城市分类工资top10
        data=self.hive_con.sql('select work_area,mon_wa from zp').toDF('work_area','salary')
        data_df=data.filter(data['work_area']!='')
        data_df.groupBy('work_area').mean().createTempView('city_sort')
        cot=1
        for i in self.spark.sql('select * from city_sort order by `avg(salary)` desc').collect():
            cs=CSrank()
            cs.id=cot
            cs.city=i[0]
            cs.salary=float(i[1])
            session.add(cs)
            cot+=1
            session.commit()
            print(i)


        #大数据职位需求量城市
        data=self.hive_con.sql('select name,work_desp,work_area,mon_wa from zp').toDF('name','work_desp','city','salary')
        datardd=data.rdd
        datardd=datardd.filter(lambda i:bigdt(i.name) or bigdt(i.work_desp))
        datadf=datardd.toDF()
        datadf.groupBy('city').count().createTempView('bigdt_city')
        datadf.groupBy('city').mean().createTempView('bigdt_salary')
        salary=self.spark.sql('select * from bigdt_salary').collect()
        # for i in salary:
        #     print(i)
        cot=1
        for i in self.spark.sql('select * from bigdt_city').collect():
            bc=BCSrank()
            bc.id=cot
            bc.name=i[0]
            bc.count=int(i[1])
            cot+=1
            for j in salary:
                if j.city==i[0]:
                    bc.salary=j[1]
            session.add(bc)
            session.commit()
            print(i)
        #大数据需求行业前10
        data = self.hive_con.sql('select name,work_desp,work_lable,mon_wa from zp').toDF('name', 'work_desp','work_lable','salary')
        datardd=data.rdd
        datardd=datardd.filter(lambda i:bigdt(i.name) or bigdt(i.work_desp))\
        .map(lambda i:Row(
            **{
                'name':i.name,
                'work_desp':i.work_desp,
                'work_lable':bigdt_lable(i.name+str(i.work_desp)+i.work_lable),
                'salary':i.salary
            }
        ))
        datadf=datardd.toDF()
        datadf.groupBy('work_lable').count().createTempView('bigdf_lable')
        datadf.groupBy('work_lable').mean().createTempView('bigdf_salary')
        mean_salary=self.spark.sql('select * from bigdf_salary').collect()
        cot=1
        for i in self.spark.sql('select * from bigdf_lable order by count desc').collect():
            bt=BDTrank()
            bt.id=cot
            bt.name=i[0]
            bt.count=int(i[1])
            # for j in mean_salary:
            #     if j[0]==i[0]:
            #         bt.salary=j[1]
            cot+=1
            # print(bt.name,bt.salary,bt.count)
            session.add(bt)
            session.commit()
            print(i)

       # IT行业需求排名
        data = self.hive_con.sql('select work_lable from zp' ).toDF('work_lable')
        datardd=data.filter(data['work_lable']!='').rdd
        datadf=self.spark.createDataFrame(datardd.map(lambda i:[lable_filter(i.work_lable)])).toDF('work_lable')
        datadf.groupBy('work_lable').count().createTempView('IT_top10')
        cot=1
        for i in self.spark.sql('select * from IT_top10 order by count desc').collect():
            if str(i[0])=='1':
                continue
            itc=ITCrank()
            itc.id=cot
            itc.name=i[0]
            itc.count=int(i[1])
            cot+=1
            session.add(itc)
            session.commit()
            print(i)

        #大数据人才类型需求排名
        data=self.hive_con.sql('select name,work_lable,mon_wa from zp').toDF('name','work_lable','salary')
        datardd=data.rdd
        datardd=datardd.filter(lambda i:bigdt(i.name) or bigdt(i.work_lable))
        datardd=datardd.map(lambda i:Row(**{
            'lable':bigdt_pp(i.name+i.work_lable),
            'name':i.name,
            'work_lable':i.work_lable,
            'salary':i.salary
        }))
        datadf=datardd.toDF()
        datadf.groupBy('lable').count().createTempView('test')
        datadf.groupBy('lable').mean().createTempView('test2')
        mean_salary=self.spark.sql('select * from test2').collect()
        cot=1
        for i in self.spark.sql('select * from test order by count desc').collect():
            bp=BPSrank()
            bp.id=cot
            bp.name=i[0]
            bp.count=int(i[1])
            cot+=1
            for j in mean_salary:
                if j[0]==i[0]:
                    bp.salary=j[1]

            session.add(bp)
            session.commit()
            print(i)
    def features_eng(self,dbname,table):
        self.hive_con.sql('use `%s` ' % dbname)
        data=self.hive_con.sql('select education,id,mon_wa,name,work_area,work_desp,work_exp,work_lable from `%s`' % table).\
            toDF('education','id','mon_wa','name','work_area','work_desp','work_exp','work_lable')
        data=data.filter(data['work_lable']!='').rdd.map(lambda i:Row(**{
            'education':str(new_edu_trans(i.education)),
            'id':i.id,
            'mon_wa':mon_wa_trans(i.mon_wa),
            'name':i.name,
            'work_area':i.work_area,
            'work_desp':i.work_desp,
            'work_exp':i.work_exp,
            'work_lable':lable_filter(i.work_lable),
            'shaixuan':lable_filter(i.work_lable)
        })).toDF()
        dataDF=data.filter(data['work_lable']!='1')
        print(dataDF.count())
        dataRDD=dataDF.rdd
        tf_idfRDD=self.tf_idf(dataRDD=dataRDD)
        model=self.NaiveByes_model(RDD=tf_idfRDD)
        # tf_idfRDD=self.features_normal(featuresRDD=tf_idfRDD)
        # self.NaiveByes_model(RDD=tf_idfRDD)
        # tf_idfRDD.foreach(print)
        # self.nd_idf(dataRDD=dataRDD)

        # model=NaiveBayesModel.load(self.sc,'hdfs://localhost:9000/qtzpnymodel')
        # agg_idfmodel=IDFModel.load('hdfs://localhost:9000/agg_idf_test')
        # nd_idfmodel=IDFModel.load('hdfs://localhost:9000/nd_idf_test')
        #
        #
        # testdata=self.hive_con.sql('select education,mon_wa,name,work_area,work_desp,work_exp,work_lable from `%s` where id=789' % table)
        # testdata=testdata.toDF('education','mon_wa','name','work_area','work_desp','work_exp','work_lable')
        # testdataRDD=testdata.rdd.map(lambda i:Row(**{
        #     'education':new_edu_trans(i.education),
        #     'salary':mon_wa_trans(i.mon_wa),
        #     'name':i.name,
        #     'city':i.work_area,
        #     'work_desp':i.work_desp,
        #     'work_exp':i.work_exp,
        #     'work_lable':i.work_lable
        # }))
        # testdataRDD.foreach(print)
        # featuresRDD=self.sample_tf_idf(dataRDD=testdataRDD,nd_idf=nd_idfmodel,agg_idf=agg_idfmodel)
        # featuresRDD=featuresRDD.map(lambda i:features_trans(i))
        # featuresRDD=featuresRDD.map(lambda i:model.predict(i.features))
        # print(featuresRDD.collect())
    def nd_idf(self,dataRDD):
        dataDF=dataRDD.map(lambda i:Row(**{
            'name_and_desp':desp_text_division(i.name+','+i.work_desp)
        })).toDF()
        tf=HashingTF(inputCol='name_and_desp',outputCol='ndFeatures',numFeatures=10240)
        idf=IDF(inputCol='ndFeatures',outputCol='ndfeatures')
        dataDF=tf.transform(dataDF)
        idf_model=idf.fit(dataDF)
        # idf_model.save('hdfs://localhost:9000/nd_idf_test')
        return idf_model

    def agg_idf(self,dataRDD):
        dataDF=dataRDD.map(lambda i:Row(**{
            'agg':[i.education]+[i.work_area]+[i.work_lable]+[i.work_exp]
        })).toDF()
        tf=HashingTF(inputCol='agg',outputCol='Features_agg',numFeatures=256)
        idf=IDF(inputCol='Features_agg',outputCol='features_agg')
        dataDF=tf.transform(dataDF)
        idf_model=idf.fit(dataDF)
        # idf_model.save('hdfs://localhost:9000/agg_idf_test')
        return idf_model


    def sample_tf_idf(self,dataRDD,nd_idf,agg_idf):
        dataDF=dataRDD.map(lambda i:Row(**{
            'salary':int(i.salary),
            'agg':[i.education]+[i.city]+[i.work_lable]+[i.work_exp],
            'name_and_desp':desp_text_division(i.name+','+i.work_desp)
        })).toDF()
        dataDF.show()
        ndtf=HashingTF(inputCol='name_and_desp',outputCol='ndFeatures',numFeatures=10240)
        aggtf=HashingTF(inputCol='agg',outputCol='Features_agg',numFeatures=256)
        data=ndtf.transform(dataDF)
        data=aggtf.transform(data)
        data.show()
        idfdata=nd_idf.transform(data)
        idfdata=agg_idf.transform(idfdata)
        idfdata.select('salary','ndfeatures','features_agg')
        RDD=idfdata.rdd
        featuresRDD=RDD.map(lambda i:(i.salary,i.ndfeatures.toArray().tolist()+i.features_agg.toArray().tolist()))
        return featuresRDD



    def tf_idf(self,dataRDD):
        dataDF=dataRDD.map(lambda i:Row(**{
                    'name_and_desp':desp_text_division(i.name+','+i.work_desp),
                    'salary':i.mon_wa,
                    'education':[i.education],
                    'city':[i.work_area],
                    'work_lable':[i.work_lable],
                    'work_exp':[i.work_exp]
        })).map(lambda i:Row(**{
            'name_and_desp':i.name_and_desp,
            'salary':i.salary,
            'agg':i.education+i.city+i.work_lable+i.work_exp
        })).toDF()
        dataDF.show()
        nd_hashingTF=HashingTF(inputCol='name_and_desp',outputCol='ndFeatures',numFeatures=10240)
        f_hashingTF=HashingTF(inputCol='agg',outputCol='Features_agg',numFeatures=256)
        tfdata=nd_hashingTF.transform(dataDF)

        tfdata=f_hashingTF.transform(tfdata)
        nd_idf=IDF(inputCol='ndFeatures',outputCol='ndfeatures')
        f_idf=IDF(inputCol='Features_agg',outputCol='features_agg')
        nd_idf_model=nd_idf.fit(tfdata)
        f_idf_model=f_idf.fit(tfdata)
        nd_idf_model.save('hdfs://localhost:9000/nd_idf')
        f_idf_model.save('hdfs://localhost:9000/agg_idf')
        tf_idfdata=nd_idf_model.transform(tfdata)
        tf_idfdata=f_idf_model.transform(tf_idfdata)
        featuresRDD=tf_idfdata.select('salary','ndfeatures','features_agg').rdd
        featuresRDD=featuresRDD.map(lambda i:(int(i.salary),i.ndfeatures.toArray().tolist()+i.features_agg.toArray().tolist()))
        return featuresRDD

    def NaiveByes_model(self,RDD):
        featuresRDD=RDD.map(lambda i:features_trans(i))
        train,test=featuresRDD.randomSplit([0.8,0.2])
        count=test.count()
        model=NaiveBayes.train(train)
        preandsalary=test.map(lambda i:(model.predict(i.features),i.label))
        print(1.0*preandsalary.filter(lambda i:int(i[0])==int(i[1])).count()/count)
        print(1.0 * preandsalary.filter(lambda i: int(i[0]) == int(i[1]) or int(i[0])-1==int(i[1]) or int(i[0])+1==int(i[1])).count() / count)
        model.save(sc=self.sc,path='hdfs://localhost:9000/zpmodel')
        return model





    def work_count(self,dataRDD):
        work_lst=[]
        for i in dataRDD.map(lambda i:i.name+','+i.work_desp).flatMap(lambda i:text_division(i))\
            .map(lambda word:(word,1)).reduceByKey(lambda a,b:a+b).map(lambda i:(i[1],i[0]))\
            .sortByKey(ascending=False).take(5000):
            work_lst.append(i[1])

        print(work_lst)


    def features_normal(self,featuresRDD):
        from pyspark.mllib.feature import Normalizer
        normalizer=Normalizer()
        featuresRDD=featuresRDD.map(lambda p:[p[0],normalizer.transform(p[1])])
        return featuresRDD







if __name__=='__main__':
    # host=input("请输入您的host地址")
    # user = input("请输入您的mysql数据库用户名：")
    # password = input("请输入您的mysql密码：")
    # dbname = input("请输入您想连接到的mysql数据库")

    # caozuo=QtzpHanld(user=user,password=password,dbname=dbname,host=host)
    caozuo=QtzpHanld()
    caozuo.create_table()
    caozuo.salary_top10()
    # caozuo.features_eng(dbname='zp',table='zp')