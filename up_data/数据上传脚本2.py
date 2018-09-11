import hdfs
from pyspark import SparkContext
from pyspark.sql import HiveContext

client=hdfs.Client("http://127.0.0.1:50070",root='/')
tar_dir=input("请输入您想放入数据的hdfs文件夹路径：")
db=input('请输入您想将输入导入到的hive数据库名：')
tablename=input('请输入您想创建的为插入数据所准备的表名：')
try:
    client.makedirs(tar_dir)
except:
    pass

client.upload(tar_dir,'./zp2.csv')
client.upload('/','./aggidf')
client.upload('/','./ndidf')
client.upload('/','./nymodel')
print(client.list('/'))
sc=SparkContext('local','test')
hive_cot=HiveContext(sparkContext=sc)
hive_cot.sql("use %s" % db)
hive_cot.sql("create table {tbname} (bh1 int,bh int,education string,id int,mon_wa float,name string,work_area string,work_desp string,work_exp string,work_lable string) row format delimited fields terminated by ',' stored as textfile location '{filepath}'".\
             format(tbname=tablename,filepath=tar_dir))
