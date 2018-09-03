import pandas as pd
from pyspark import SparkContext

sc=SparkContext('local','test')
csv_df = pd.read_csv(str('/media/hadoop/code/招聘信息处理/screen_e.csv'))
func = lambda i: csv_df.loc[i]
info_list = [func(i) for i in range(csv_df.shape[0])]
insert_list = []
for i in info_list:
    ele_list = []
    ele_list.append(i['Unnamed: 0'])
    ele_list.append('work')
    ele_list.append('desp')
    ele_list.append(str(i['work_desp']))
    ele_tuple = (i['Unnamed: 0'], ele_list)
    insert_list.append(ele_tuple)
print('csv文件转换完成')

table = 'dbzlzp'
host = 'localhost'
keyConv = 'org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter'
valueConv = 'org.apache.spark.examples.pythonconverters.StringListToPutConverter'
conf = {"hbase.zookeeper.quorum": host, "hbase.mapred.outputtable": table,
        "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
        "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
        "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}
sc.parallelize(insert_list).saveAsNewAPIHadoopDataset(
    conf=conf, keyConverter=keyConv, valueConverter=valueConv
)