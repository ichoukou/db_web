import pandas as pd
from pyspark import SparkContext
class OperationHbase(object):
    def __init__(self):
        self.sc=SparkContext('local','test')

    def get_hbase_data(self,tablename):
        table=str(tablename)
        host='localhost'
        conf = {"hasbe.zookeeper.quorum": host, "hbase.mapreduce.inputtable": table}
        keyConv='org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter'
        valueConv='org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter'
        hbase_rdd=self.sc.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
                                          "org.apache.hadoop.hbase.io.ImmutableBytesWritable","org.apache.hadoop.hbase.client.Result",
                                     keyConverter=keyConv,
                                     valueConverter=valueConv,
                                      conf=conf)
        count=hbase_rdd.count()
        hbase_rdd.cache()
        output=hbase_rdd.collect()
        for k,v in output:
            print(k,v)

    def insert_hbase(self,tablename,datalist):
        table=str(tablename)
        host='localhost'
        keyConv = 'org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter'
        valueConv = 'org.apache.spark.examples.pythonconverters.StringListToPutConverter'
        conf = {"hbase.zookeeper.quorum": host, "hbase.mapred.outputtable": table,
                "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
                "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
        self.sc.parallelize(datalist).\
            map(lambda p:(p[0],p.split('ê ē')))\
            .saveAsNewAPIHadoopDataset(
            conf=conf,keyConverter=keyConv,valueConverter=valueConv
        )

    def csv_to_tuple(self,csvpath):
        csv_df=pd.read_csv(str(csvpath))
        func=lambda i:csv_df.loc[i]
        info_list=[func(i) for i in range(csv_df.shape[0])]
        insert_list=[]
        for i in info_list:
            # ele_list = []
            # ele_list.append(int(i['Unnamed: 0']))
            # ele_list.append('work')
            # ele_list.append('desp')
            # ele_list.append(str(i['work_desp']))
            # ele_tuple=(i['Unnamed: 0'],ele_list)
            ele=str(i['Unnamed: 0'])+'ê ē'+'work'+'ê ē'+'desp'+'ê ē'+str(i['work_desp'])
            insert_list.append(ele)
        print('csv文件转换完成')
        return insert_list




if __name__=='__main__':
    screen_e_file = '/media/hadoop/code/招聘信息处理/screen_e.csv'
    caozuo=OperationHbase()
    desp_list=caozuo.csv_to_tuple(screen_e_file)
    caozuo.insert_hbase('zlzp',desp_list)
