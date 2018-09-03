from pyspark.sql import HiveContext
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import Row,StructField,StringType,StructType,IntegerType,ArrayType,FloatType
from tools import text_division,edu_trans,work_exp_trans,mon_wa_trans,features_trans,acc_rate
from pyspark.ml.feature import HashingTF,IDF
from pyspark.mllib.classification import NaiveBayes


class TextHanld(object):
    def __init__(self):
        self.sc=SparkContext('local','test')
        self.hive_content=HiveContext(self.sc)
        self.spark=SparkSession.builder.getOrCreate()

    def mon_wa_top10(self):             #月薪前10职位
        self.hive_content.sql('use dbzlzp')
        text_data=self.hive_content.sql('select * from screen3').collect()
        # text_data.foreach(print)
        data_list=[]
        for i in text_data:
            ele_list=[]
            ele_list.append(i.leibie)
            ele_list.append(int(i.mon_wa))
            data_list.append(ele_list)

        rowRDD=self.sc.parallelize(data_list).map(lambda ele:Row(ele[0],ele[1]))
        schemaString='leibie mon_wa'
        fields=[StructField('leibie',StringType(),nullable=True),StructField('mon_wa',IntegerType(),nullable=True)]
        schema=StructType(fields)
        mon_wa_df=self.spark.createDataFrame(rowRDD,schema).groupBy('leibie').mean()
        mon_wa_df.createOrReplaceTempView('leibiecount')
        sort_result=self.spark.sql('select * from leibiecount order by `avg(mon_wa)` desc').show(1000)

    def feature_eng(self,dbname,tablename):         #特征工程
        self.hive_content.sql('use `%s`' % dbname)
        data=self.hive_content.sql('select * from `%s`' % tablename)
        dataRDD=data.rdd
        data_df=data.toDF('index', 'education', 'leibie','mon_wa', 'name', 'work_area', 'work_exp','work_lable')
        # data_df.groupBy('education').count().show(100)
        # dataRDD.foreach(print)

        # self.work_lable_summary(data=data)
        # self.info_merge(dataRDD)
        # self.word_count(dataRDD)

        #
        # mergeRDD=self.info_merge(dataRDD=dataRDD)
        # featuresRDD=self.tf_idf(mergeRDD)
        # self.Naivebayes_model(featuresRDD=featuresRDD)

        mergeRDD = self.info_merge(dataRDD=dataRDD)
        nl_idfModel=self.nl_idf(mergeRDD)
        ece_idfModel=self.ece_idf(mergeRDD)
        sample_data=self.sample_tf_idf(mergeRDD=mergeRDD,nl_idfModel=nl_idfModel,ece_idfModel=ece_idfModel)
        model=self.Naivebayes_model(featuresRDD=sample_data)


        # featuresRDD=self.features_normal(featuresRDD=featuresRDD)
        # self.Naivebayes_model(featuresRDD=featuresRDD)
        # self.ml_features_normal(features=featuresRDD)

        test_data=self.sc.parallelize([['本科','算法工程师',6000,'java开发','青岛','无经验','sssss']])
        test_data.foreach(print)
        test_data=test_data.map(lambda i:Row(**{
            'education':i[0],
            'leibie':i[1],
            'mon_wa':i[2],
            'name':i[3],
            'work_area':i[4],
            'work_exp':i[5],
            'work_lable':i[6]
        }))
        test_merge=self.info_merge(dataRDD=test_data)
        test_RDD=self.sample_tf_idf(mergeRDD=test_merge,nl_idfModel=nl_idfModel,ece_idfModel=ece_idfModel)
        test_RDD=test_RDD.map(lambda i:features_trans(i))
        test_RDD.map(lambda point:model.predict(point.features)).foreach(print)

    def Naivebayes_model(self,featuresRDD):
        featuresRDD =featuresRDD.map(lambda i:features_trans(i))
        train,test=featuresRDD.randomSplit([0.8,0.2])
        count=test.count()
        model=NaiveBayes.train(train,1.0)
        # model.save(sc=self.sc,path='hdfs://localhost:9000/mltest')
        scoresAndLabels=test.map(lambda point:[model.predict(point.features),point.label])
        # scoresAndLabels.foreach(print)
        print(1.0*scoresAndLabels.filter(lambda x:x[0]==x[1]).count()/count)
        # for i in scoresAndLabels.filter(lambda x:acc_rate(x)==False).collect():
        #     print(i)
        return model

    def tf_idf(self, mergeRDD):
        fields = [StructField('lable', IntegerType(), nullable=True),
                  StructField('edu_city_exp', ArrayType(elementType=StringType()), nullable=True),
                  StructField('leibie_name', ArrayType(elementType=StringType()), nullable=True)]
        schema = StructType(fields)
        rowRDD = mergeRDD.map(lambda p: Row(p[0], p[1], p[2]))
        info_df = self.spark.createDataFrame(schema=schema, data=rowRDD).toDF('lable', 'edu_city_exp',
                                                                              'leibie and name')
        info_df.show()
        name_df = info_df.select('lable', 'edu_city_exp', 'leibie and name')
        nl_hashingTF = HashingTF(inputCol='leibie and name', outputCol='nlFeatures', numFeatures=256)
        featurizeData = nl_hashingTF.transform(name_df)
        ece_hashingTF = HashingTF(inputCol='edu_city_exp', outputCol='eceFeatures', numFeatures=64)
        featurizeData = ece_hashingTF.transform(featurizeData)
        nl_idf = IDF(inputCol='nlFeatures', outputCol='nlfeatures')
        ece_idf = IDF(inputCol='eceFeatures', outputCol='ecefeatures')
        nl_idfModel = nl_idf.fit(featurizeData)
        ece_idfModel = ece_idf.fit(featurizeData)
        rescaledData = nl_idfModel.transform(featurizeData)
        rescaledData = ece_idfModel.transform(rescaledData)
        tf_idfmerge = []
        for i in rescaledData.select('lable', 'nlfeatures', 'ecefeatures').collect():
            ele_lst = i.nlfeatures.toArray().tolist() + i.ecefeatures.toArray().tolist()
            tf_idfmerge.append((int(i.lable), ele_lst))
        print(tf_idfmerge)

        featuresRDD = self.sc.parallelize(tf_idfmerge)
        return featuresRDD


    def sample_tf_idf(self,mergeRDD,nl_idfModel,ece_idfModel):
        dataDF=mergeRDD.map(lambda p:Row(**{
            'lable':p[0],
            'edu_city_exp':p[1],
            'leibie and name':p[2]
        })).toDF()
        nl_hashingTF = HashingTF(inputCol='leibie and name', outputCol='nlFeatures', numFeatures=256)
        featuresData = nl_hashingTF.transform(dataDF)
        ece_hashingTF = HashingTF(inputCol='edu_city_exp', outputCol='eceFeatures', numFeatures=64)
        featuresData = ece_hashingTF.transform(featuresData)
        rescled=nl_idfModel.transform(featuresData)
        rescled=ece_idfModel.transform(rescled)
        RDD=rescled.rdd
        featuresRDD=RDD.map(lambda i:(i.lable,i.nlfeatures.toArray().tolist()+i.ecefeatures.toArray().tolist()))
        return featuresRDD

    def nl_idf(self,mergeRDD):
        dataDF=mergeRDD.map(lambda p:Row(**{
            'leibie and name':p[2]
        })).toDF()
        nl_hashingTF=HashingTF(inputCol='leibie and name',outputCol='nlFeatures',numFeatures=256)
        featuresData=nl_hashingTF.transform(dataDF)
        nl_idf=IDF(inputCol='nlFeatures',outputCol='nlfeatures')
        nl_idfModel=nl_idf.fit(featuresData)
        return nl_idfModel

    def ece_idf(self,mergeRDD):
        dataDF=mergeRDD.map(lambda p:
                            Row(**{
                                'edu_city_exp':p[1]
                            })).toDF()
        ece_hashingTF=HashingTF(inputCol='edu_city_exp',outputCol='eceFeatures',numFeatures=64)
        featuresData=ece_hashingTF.transform(dataDF)
        ece_idf=IDF(inputCol='eceFeatures',outputCol='ecefeatures')
        ece_idfModel=ece_idf.fit(featuresData)
        return ece_idfModel



    def work_lable_summary(self,data):          #标签汇总,传入一个查询数据表
        lable_list=data.rdd.map(lambda i:i.work_lable).collect()
        duplicate_remove_lst=[]
        for i in lable_list:
            for j in str(i).split(','):
                if j not in duplicate_remove_lst:
                    duplicate_remove_lst.append(j)
                else:
                    continue
        print(duplicate_remove_lst)


    def info_merge(self,dataRDD):       #信息合并,将一个多列rdd合并成单列rdd,方便机器学习
        edu_area_exp_list = []
        leibie_name_list = []
        mon_wa_list = []
        # name_list = []
        work_lable_list = []

        educationRDD = dataRDD.map(lambda i: i.education).map(lambda i: edu_trans(i))
        edu_collect = educationRDD.collect()
        work_areaRDD = dataRDD.map(lambda i: i.work_area)
        work_area_collect = work_areaRDD.collect()
        for i,j in zip(edu_collect,work_area_collect):
            ele_lst=[]
            ele_lst.append(i)
            ele_lst.append(j)
            edu_area_exp_list.append(ele_lst)
        # print('work_areawancheng')
        work_expRDD = dataRDD.map(lambda i: i.work_exp).map(lambda i: work_exp_trans(i))
        work_exp_collect = work_expRDD.collect()
        for i,j in zip(edu_area_exp_list,work_exp_collect):
            i.append(j)
        # print('education wancheng')
        leibieRDD = dataRDD.map(lambda i: i.leibie).map(lambda i:text_division(i))
        leibie_collect = leibieRDD.collect()
        nameRDD = dataRDD.map(lambda i: i.name).map(lambda i: text_division(i))
        name_collect = nameRDD.collect()
        for i,j in zip(name_collect,leibie_collect):
            leibie_name_list.append(i+j)
        print(len(leibie_name_list))
        # print('leibiewancheng')
        mon_waRDD = dataRDD.map(lambda i: i.mon_wa).map(lambda i: mon_wa_trans(i))
        # print('mon_wawancheng')
        mon_wa_collect = mon_waRDD.collect()
        for i in mon_wa_collect:
            mon_wa_list.append(i)
        print(len(mon_wa_list))

        # print('namewancheng')

        # print('work_expwancheng')
        work_lableRDD = dataRDD.map(lambda i: i.work_lable).map(lambda i: str(i).split(','))
        work_lable_collect = work_lableRDD.collect()
        for i in work_lable_collect:
            work_lable_list.append(i)
        print(len(work_lable_list))
        merge_lst=[]
        for i in range(len(mon_wa_list)):
            ele_lst=[]
            ele_lst.append(mon_wa_list[i])
            ele_lst.append(edu_area_exp_list[i])
            ele_lst.append(leibie_name_list[i])
            ele_lst.append(work_lable_list[i])
            merge_lst.append(ele_lst)
        mergeRDD=self.sc.parallelize(merge_lst)
        return mergeRDD


    def word_count(self,dataRDD):
        leibieRDD = dataRDD.map(lambda i: i.leibie).flatMap(lambda i: text_division(i)).map(lambda word:(str(word).lower(),1)).reduceByKey(lambda a,b:a+b).\
            map(lambda i:(i[1],i[0])).sortByKey(ascending=False).take(500)
        work_lableRDD = dataRDD.map(lambda i: i.work_lable).flatMap(lambda i: str(i).split(',')).map(lambda word:(str(word).lower(),1)).reduceByKey(lambda a,b:a+b).\
            map(lambda i:(i[1],i[0])).sortByKey(ascending=False).take(500)
        nameRDD = dataRDD.map(lambda i: i.name).flatMap(lambda i: text_division(i)).map(lambda word:(str(word).lower(),1)).reduceByKey(lambda a,b:a+b).\
            map(lambda i:(i[1],i[0])).sortByKey(ascending=False).take(500)
        cityRDD=dataRDD.map(lambda i:i.work_area).map(lambda word:(word,1)).reduceByKey(lambda a,b:a+b).map(lambda i:(i[1],i[0]))\
            .sortByKey(ascending=False).take(500)
        # print(leibieRDD)
        # print(work_lableRDD)
        # print(nameRDD)
        print(len(cityRDD))

    def features_normal(self,featuresRDD):
        from pyspark.mllib.feature import Normalizer
        # featuresRDD=featuresRDD.map(lambda point:Row(point.label,point.features))
        # fields=[StructField('label',FloatType(),nullable=True),StructField('features',ArrayType(elementType=FloatType()),nullable=True)]
        # schema=StructType(fields)
        fl_df=self.spark.createDataFrame(featuresRDD).toDF('label','features')
        # fl_df.foreach(print)
        # scaler=MinMaxScaler(inputCol='features',outputCol='SCfeatures')
        # scalerModel=scaler.fit(fl_df)
        # SCdata=scalerModel.transform(fl_df).select('label','SCfeatures')
        # SCdata.foreach(print)
        normalizer=Normalizer()
        featuresRDD=featuresRDD.map(lambda p:[p[0],normalizer.transform(p[1])])
        # featuresRDD=featuresRDD.map(lambda p:LabeledPoint(int(p[0]),p[1]))
        return featuresRDD

    def ml_features_normal(self,features):
        from pyspark.ml.linalg import Vectors
        from pyspark.ml.feature import Normalizer
        from pyspark.ml.classification import NaiveBayes
        from tools import f
        features.foreach(print)
        fea_df=features.map(lambda i:Row(**f(i))).toDF()
        # fea_df.show()
        normalizer=Normalizer().setInputCol('features').setOutputCol('norfeatures').setP(1.0)
        norfea_df=normalizer.transform(fea_df)
        # norfea_df.show()
        train_dt,test_dt=norfea_df.randomSplit([0.8,0.2])
        nvby=NaiveBayes(modelType="multinomial",smoothing=0.1)
        nvby_mod=nvby.fit(dataset=train_dt)

        predictRDD=nvby_mod.transform(test_dt).rdd
        count=predictRDD.count()
        print(predictRDD.map(lambda i:(i.label,i.prediction)).filter(lambda i:i[0]==i[1]).count()/count)
        # normalizer=Normalizer().setInputCol('features').setOutputCol('norfeatures').setP(1.0)
        # nor_feadf=normalizer.transform(fea_df)
        # train_dt,test_dt=nor_feadf.randomSplit([0.7,0.3])
        # nvby=NaiveBayes().setLabelCol('lable').setFeaturesCol('features')
        # nvby_mod=nvby.fit(train_dt)
        # predictionRDD=nvby_mod.transform(test_dt).rdd
        # count=predictionRDD.count()
        # print(predictionRDD.map(lambda i:[int(i.lable),int(i.prediction)]).filter(lambda i:i[0]==i[1]).count()/count)
        # nvby=NaiveBayes().setLabelCol('lable').setFeaturesCol('norfeatures')
        # nvby_mod = nvby.fit(train_dt)
        # predictionRDD = nvby_mod.transform(test_dt).rdd
        # count = predictionRDD.count()
        # print(predictionRDD.map(lambda i: [int(i.lable), int(i.prediction)]).filter(
        #     lambda i: i[0] == i[1]).count() / count)
        # # nor_feadf.show()

if __name__=='__main__':
    TextHanld().feature_eng(dbname='dbzlzp',tablename='screen3')
    # TextHanld().mon_wa_top10()

