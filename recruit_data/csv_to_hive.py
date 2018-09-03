import pandas as pd
from pyspark.sql import HiveContext
from pyspark.sql.types import Row,StringType,StructField,IntegerType,StructType
from pyspark.sql import SparkSession
from pyspark import SparkContext

screen_e_file='./screen_e.csv'

list1=['普工/操作工','销售代表','工程造价/预结算','学徒工','技工','游戏策划','工程监理/质量管理','网络/在线销售','助理/秘书/文员','组装工',
           '送餐员','储备干部','智能大厦/布线/弱电/安防','建筑工程测绘/测量','项目专员/助理','人力资源主管','搬运工','文档/资料管理','机械维修/保养',
           '机电工程师','多媒体/动画设计','销售总监','网络/在线客服','网络与信息安全工程师','行政专员/助理','人力资源专员/助理','客户服务专员/助理',
           '培训生','施工员','车床/磨床/铣床/冲床工','环保技术工程师','售前/售后技术支持管理','电话销售','土木/土建/结构工程师',
           '仪器/仪表/计量工程师','生产主管/督导/组长','水利/水电工程师','机械工程师','生产物料管理（PMC）','电工','电脑操作/打字/录入','项目经理/项目主管',
           '兼职','客户代表','理货/分拣/打包','给排水/暖通/空调工程','客户咨询热线/呼叫中心人员','仓库/物料管理员','美术编辑/美术设计','电焊工/铆焊工',
           '模具工','招聘专员/助理', '物流专员/助理', '后勤人员', '化工工程师', '项目招投标', '模具工程师', '需求工程师', '人力资源经理','员工关系/企业文化/工会',
        '网络运营专员/助理', '服务员', '建筑工程安全管理', 'Helpdesk', '道路/桥梁/隧道工程技术', '机械设备工程师', '采购专员/助理', '招聘经理/主管', '互联网产品专员/助理', '市场专员/助理', '业务拓展专员/助理', '前台/总机/接待', '建筑工程师', 'CAD设计/制图', '店员/营业员/导购员', '能源/矿产项目管理', '新媒体运营', '水处理工程师', '防损员/内保', '电子商务专员/助理', '园林/景观设计', '视觉设计', '厨师助理/学徒', '快递员/速递员', '演员/模特', '化学分析', '机械设计师', 'IT项目经理/主管', '生物工程/生物制药', '建筑施工现场管理', '汽车维修/保养'
        , '销售经理', '内勤人员', '教学/教务管理人员', '产品运营', '商务专员/助理', '机械制图员', '文字编辑/组稿', '副总裁/副总经理', '语音/视频/图形开发', '有线传输工程师', '供应商/采购质量管理', 'CTO/CIO', '汽车电子工程师', '英语翻译', '房地产销售/置业顾问', '计算机辅助设计师', '会计/会计师', '保安', '销售数据分析', '质量管理/测试经理', '导游/票务', '销售主管', '后期制作',
           '室内装潢设计', '呼叫中心客服', '质量管理/测试主管', '旅游计划调度', '化验/检验', '数控操作', '安全消防', '信息技术标准化工程师', '培训师/讲师', '日语翻译', '电气设计',
           '生产设备管理', '销售行政专员/助理', '工业工程师', '总编/副总编', '石油/天然气技术人员', '材料工程师', '政府事务管理', '幼教',
           '微信推广', '合伙人', 'Flash设计/开发', '钳工/机修工/钣金工', '市场营销专员/助理', '制造工程师', '电子元器件工程师', '审计专员/助理', '建筑设计师', '市场调研与分析',
           '认证/体系工程师/审核员','原画师', '大客户销售代表','区域销售专员/助理', '审计经理/主管', '证券分析/金融研究', '激光/光电子技术', '化学实验室技术员/研究员', '培训/招生/课程顾问', '物业管理专员/助理', '外贸/贸易专员/助理', '临时', '护士/护理人员', '化学技术应用', '工业设计', '城市规划与设计', '现场应用工程师（FAE）', '安检员', '生产运营管理', '医药代表', '培训专员/助理', '报关员', '水工/木工/油漆工', '外卖快递', '网店运营', '体育老师/教练', '万能工', '注塑工程师', '互联网产品经理/主管', '电子/电器项目管理', '销售业务跟单', '仿真应用工程师', '物流/仓储调度', '工程资料管理', '网店客服', '金融/经济研究员', '机修工', '统计员', '建筑制图', '销售工程师', '会计助理/文员', '党工团干事', '产品专员/助理', '策略发展总监', '环境/健康/安全工程师', 'IT质量管理经理/主管', '地质勘查/选矿/采矿', '汽车销售', '广告创意/设计师', '地勤人员', '部门/事业部管理', '水利/港口工程技术', '产品管理', '物料主管/专员', '农艺师', '服装/纺织品设计', '机械研发工程师', '风险管理/控制/稽查', '工程总监', '内容运营', '音频/视频工程师/技术员', '机械工艺/制程工程师', '焊接工程师/技师', '电力电子研发工程师', '设计管理人员', '环境监测工程师', '电力工程师/技术员', '酒店管理', '网站推广', '空调/热能工程师', '客户经理', '标准化工程师', '包装工', '调研员', '机动车司机/驾驶', '船舶设计与制造', '运营主管/专员', '光源/照明工程师', '财务分析员', '射频工程师', '电池/电源开发', '视频主播', '监控维护', '市场策划/企划专员/助理', '网店管理员', '行政经理/主管/办公室主任', '林业技术人员', '园艺师', '知识产权/专利顾问/代理人', '教育产品开发', '业务拓展经理/主管', '项目总监', '餐厅服务员', '仓库经理/主管', '出纳员', 'IT技术/研发经理/主管', '客户服务经理', '配置管理工程师', '房地产项目管理', '咨询项目管理', '银行柜员', '绘画', '供应商开发', '客户关系/投诉协调人员', '前厅接待/礼仪/迎宾', '总裁助理/总经理助理', '物流销售', '畜牧师', '空调工/电梯工/锅炉工', '渠道/分销专员', '财务助理', '岩土工程', '招商专员', '咨询顾问/咨询员', '机械结构工程师', '作家/编剧/撰稿人', '电信交换工程师', '贸易跟单', '船舶驾驶/操作', '影视策划/制作人员', '信息技术经理/主管',
           '艺术/设计总监', '汽车零部件设计师', '订单处理员', '广告美术指导', '高级建筑工程师/总工', '薪酬福利专员/助理', '安防系统工程师', '技术研发工程师', '核保理赔', '市场文案策划',
           '绩效考核专员/助理', '汽车机械工程师', '房地产中介/交易', '废气处理工程师', '区域销售经理/主管', '证券/期货/外汇经纪人', '生产文员', '技术文档工程师', '健身/美体/舞蹈教练',
           '选址拓展/新店开发', '化工研发工程师', '传菜员', '情报信息分析', '物业维修', '旅游产品/线路策划', '模拟电路设计/应用工程师', '厨师/面点师', '活动策划', '生产跟单',
           '软装设计师', '售后服务/客户服务', '大堂经理/领班', '配音员', '广告客户经理', '飞机设计与制造', '销售运营专员/助理', '生产项目工程师', '土建勘察', '版图设计工程师',
           '房地产内勤', '渠道/分销经理/主管', 'IT技术/研发总监', '控制保护研发工程师', '通信电源工程师', '会务专员/助理', '印刷操作', '活动执行', '人力资源总监', 'IT项目总监',
           '银行大堂经理', '市场经理', '手机维修', '喷塑工', '市场策划/企划经理/主管', '房地产客服', '环境/健康/安全经理/主管', '园林景观设计师', '旅游顾问', '淘宝/微信运营专员/主管',
           '投资/理财服务', '企业培训师/讲师', '设备主管', '电器研发工程师', '导演/编导', '会展策划/设计', '保险代理/经纪人/客户经理', '团购业务员', '公关专员/助理',
           '药品生产/质量管理', '保险内勤', '飞机驾驶/操作', '装配工程师/客户经理', '空调工程/设计', '业务分析专员/助理', '电声/音响工程师/技术员', '摄影师/摄像师', '广告客户代表',
           '排版设计', '仪表工', '气动工程师', '汽车电工', '外语教师', '采购材料/设备管理', '经纪人/星探', '主持人/司仪', '房地产评估', '印刷排版/制版', '金融产品销售',
           '公交/地铁乘务', '职业技术教师', '店面/展览/展示/陈列设计', '公务员/事业单位人员', '通信标准化工程师', '杂工', '施工队长', '无损检测工程师', '文案策划', '品牌策划',
           '物流经理/主管', '环境评价工程师', '市政工程师', '生态治理/规划', '美发/发型师', '环境管理/园林景区保护', '货运代理', '架线和管道工程技术', '医疗管理人员', '机械设备经理',
           '厨工', '社会工作者/社工', '收银员', '媒介专员/助理', '家具设计', '区域销售总监', '财务顾问', '首席运营官COO', '店长/卖场管理', '首席财务官CFO', '媒介策划/管理',
           '信用卡销售', '销售培训师/讲师', '汽车装饰美容', '电力线路工', '故障分析工程师', '理货员', '插花设计师', '财务主管/总帐主管', '广告文案策划', '企业秘书/董事会秘书',
           '猎头顾问/助理', '医药化学分析', '工程机械经理', '临床协调员', '印刷机械机长', '咨询师', '项目管理', '银行会计/柜员', '锅炉工程师/技师', '初中教师', '图书管理员',
           '汽车质量管理/检验检测', '包装工程师', '财务经理', '产品总监', '广告客户主管', '供应链管理', '缝纫工', '技术研发经理/主管', '信审核查', '采购经理/主管',
           '汽车定损/车险理赔', '产品策划工程师', '药品研发', '税务专员/助理', '理科教师', '工艺品/珠宝设计', '广告制作执行', '销售运营经理/主管', '核力/火力工程师', '培训督导',
           '生产经理/车间主任', '动物营养/饲料研发', '融资专员/助理', '音效师', '家居用品设计', '促销员', '动物育种/养殖', '渠道/分销总监', '固废处理工程师', '运营总监', '网店推广',
           '专业顾问', '清算人员', '银行客户经理', 'IT文档工程师', '客房服务员', '营运经理', '瓦工', '保洁', '首席执行官CEO/总裁/总经理', '高中教师', '会籍顾问',
           '冲压工程师/技师', '增值产品开发工程师', '化学操作', '市场主管', '成本会计', '韩语/朝鲜语翻译', '医药技术研发人员', '网站运营总监/经理', '税务经理/主管', '食品/饮料研发',
           '证券/投资客户代表', '夹具工程师', '临床数据分析员', '兼职教师', '广告/会展业务拓展', '证券/投资客户经理', '可靠度工程师', '小学教师', '调酒师/茶艺师/咖啡师', '配色工',
           '加油站工作员', '品牌专员/助理', '市场运营', '平面设计经理/主管', '房地产项目策划专员/助理', '二手车评估师', '融资总监', 'VIP专员', '变压器与磁电工程师', '化学制剂研发',
           '市场总监', '成本经理/主管', '绩效考核经理/主管', '线路结构设计', '物业租赁/销售', '其他语种翻译', '纸样师/车板师', '证券/投资项目管理', '列车乘务', '医疗器械研发',
           '业务分析经理/主管', '西点师', '舞蹈老师', '资产/资金管理', '生产项目经理/主管', '飞机维修/保养', '股票/期货操盘手', '招商主管', '财务总监', '水运/空运/陆运操作',
           '销售行政经理/主管', '电梯工', '公关经理/主管', '转播工程师', '交通管理员', '信托服务', '宠物护理和美容', '物流/仓储项目管理', '团购经理/主管', '地铁轨道设计',
           '广告/会展项目管理', '食品加工/处理', '工装工程师', '车身设计工程师', '经销商', '会计经理/主管', '客户服务主管', '汽车底盘/总装工程师', '大客户销售经理', '化学/化工技术总监',
           '海外游计调', '救生员', '塑料工程师', '助理业务跟单', '物业顾问', '电力系统研发工程师', '珠宝/收藏品鉴定', '轨道交通工程师/技术员', '光伏系统工程师', '电分操作员',
           '幕墙工程师', '投资经理', '烧烤师', '房地产销售主管', '潜水员', '工程机械主管', '投资者关系', '维修经理/主管', '品牌主管', '培训助理/助教', '化验师', '钟点工',
           '家政人员', '营运主管', '服装打样/制版', '保安经理', '学术推广', '电脑放码员', '航空乘务', '医学影像/放射科医师', '楼面管理', '放映管理', '饲料销售',
           '服装/纺织品/皮革质量管理', '电子商务总监', '面料辅料开发/采购', '客户主管', '企业/业务发展经理', '油漆/化工涂料研发', '保姆/母婴护理', '银行客户服务', '外籍教师',
           '金融产品经理', '服装/纺织品/皮革销售', '编辑出版', '发行管理', '服装/纺织/皮革跟单', '临床研究员', '汽车/摩托车工程师', '汽车工程项目管理', '签证业务办理',
           '信贷管理/资信评估/分析', '中餐厨师', '家电维修', '咨询经理/主管', '监察人员', '地产店长/经理', '大学教师', '船务/空运陆运操作', '汽车零配件销售', '品牌经理',
           '食品/饮料检验', '铸造/锻造工程师/技师', '玩具设计', '成本管理员', '风险控制', '法务专员/助理', '校长/副校长', '音乐教师', '医药技术研发管理人员', '财务分析经理/主管',
           '汽车装配工艺工程师', '融资经理/主管', '房地产销售经理', '化妆师/造型师/服装/道具', '市场营销主管', 'IC验证工程师', '包装设计', '餐厅领班', '美容师/美甲师',
           '薪酬福利经理/主管', '房地产项目配套工程师', '化工项目管理', '志愿者/义工', '无线电工程师', '针灸/推拿', '招商经理', '铲车/叉车工', '工厂厂长/副厂长',
           '汽车售后服务/客户服务', '基金项目经理', '医疗器械推广', '买手', '洗碗工', '项目计划合约专员', '生产总监', '实验室负责人/工程师', '船舶乘务', '行李员', '印染工',
           '商务经理/主管', '配色技术员', '服装/纺织/皮革工艺师', '灯光师', '产品经理', '护理主任/护士长', '记者/采编', '美术教师', '汽车机构工程师', '家教', '复卷工',
           '广告创意/设计总监', '合同管理', '金融服务经理', '单证员', '房地产项目开发报建', '水运/陆运/空运销售', '校对/录入', '综合业务专员/助理', '培训经理/主管',
           '企业律师/合规经理/主管', '高级客户经理/客户经理', '会务经理/主管', '服装/纺织/皮革项目管理', '合规经理', '预订员', '眼科医生/验光师', '旅游产品销售', '储备经理人',
           '分公司/代表处负责人', '法语翻译', '游泳教练', '外汇交易', '婚礼/庆典策划服务', '艺术指导/舞美设计', '总工程师/副总工程师', '促销主管/督导', '人事信息系统(HRIS)管理',
           '运输经理/主管', '广告客户总监', '按摩/足疗', '奢侈品销售', '瑜伽教练', '意大利语翻译', '外科医生', '网店店长', '美容顾问(BA)', '保险培训师', '物料经理',
           '医药学术推广', '医药项目管理', '行政总监', '资金专员', '医疗器械生产/质量管理', '汽车动力系统工程师', '纺织工/针织工', '剪裁工', '保险电销', '集装箱业务', '客房管理',
           '专科医生', '房地产资产管理', '主笔设计师', '户外/游戏教练', '物业经理/主管', '西餐厨师']
list2=['售前/售后技术支持工程师','质量检验员/测试员','其他','科研人员','生产计划',]
list3=['UI','网页','游戏','web','ui','java','python','.net','C#','C语言','C++','c语言','c++','c#','JAVA','PYTHON','.NET'
       ,'php','PHP','App','app','APP','数据库','MySQL','mysql','MYSQL','Web','sql','程序','vr','数据','seo','linux','安卓','ios',
           '通信','网络工程',]
web_list=['网页','web','h5']
app_list=['app',]
C_list=['c语言','c++',]
db_list=['mysql','sql','数据库',]
ruanjian_list=['c#','.net','python']
java_list=['java']
php_list=['php']
bd_deeple=['大数据','人工智能','深度学习']
qianru_list=['嵌入']

class CsvToHive(object):

    def __init__(self):
        self.sc=SparkContext('local','test')
        self.hive_context=HiveContext(self.sc)
        self.spark=SparkSession.builder.getOrCreate()


    def read_csv_to_list(self,filepath):
        csv_df=pd.read_csv(str(filepath))
        func=lambda i:csv_df.loc[i]
        info_list=[func(i) for i in range(csv_df.shape[0])]
        insert_list=[]
        for i in info_list:
            ele_list = []
            ele_list.append(i['Unnamed: 0'])
            ele_list.append(str(i['education']))
            ele_list.append(str(i['leibie']))
            ele_list.append(str(i['mon_wa']))
            ele_list.append(str(i['name']))
            ele_list.append(str(i['work_area']))
            ele_list.append(str(i['work_exp']))
            ele_list.append(str(i['work_lable']))
            insert_list.append(ele_list)
        print('csv文件转换完成')
        return insert_list

    def list_to_hive(self,data_list,tablename):

        infoRDD=self.spark.sparkContext.parallelize(data_list)
        infoRDD.foreach(print)
        schema=StructType([StructField("index",IntegerType(),True),StructField("education",StringType(),True),
                           StructField("leibie",StringType(),True),StructField("mon_wa",StringType(),True),
                           StructField("name",StringType(),True),StructField("work_area",StringType(),True),
                           StructField("work_exp",StringType(),True),StructField("work_lable",StringType(),True)])

        rowRDD=infoRDD.map(lambda p:Row(int(p[0]),p[1],p[2],p[3],p[4],
                                        p[5],p[6],p[7]))
        infoDF=self.spark.createDataFrame(rowRDD,schema)
        infoDF.registerTempTable('temptable')
        self.hive_context.sql('use dbzlzp')
        self.hive_context.sql('insert into %s select * from temptable' % str(tablename))
        print('数据插入完成')
    def select_hive_data(self,db,tablename):
        self.hive_context.sql('use %s' % str(db))
        self.hive_context.sql('select * from %s' % str(tablename)).show()


    def mon_wa_pro(self):
        self.hive_context.sql('use dbzlzp')
        mon_was=self.hive_context.sql('select * from screnn').collect()
        cot=0
        data_list=[]
        index = 0
        for i in mon_was:
            ele_list=[]
            mon_walist=i.mon_wa.split('-')
            if len(mon_walist)!=2:
                continue
            elif '实习' in str(i.name) or '实习' in str(i.leibie):
                continue
            elif int(mon_walist[0])%10!=0:
                mon_walist[0]=int(10*(int(mon_walist[0])//10))
                mon_walist[1]=int(mon_walist[1])
                mon_wa_value=(mon_walist[0]+mon_walist[1])/2
                ele_list.append(index)
                ele_list.append(i.education)
                ele_list.append(i.leibie)
                ele_list.append(str(int(mon_wa_value)))
                ele_list.append(i.name)
                ele_list.append(i.work_area)
                ele_list.append(i.work_exp)
                ele_list.append(i.work_lable)
                data_list.append(ele_list)
                index+=1
                # print(mon_wa_value)
            else:
                mon_walist[0]=int(mon_walist[0])
                mon_walist[1]=int(mon_walist[1])
                mon_wa_value=(mon_walist[0]+mon_walist[1])/2
                ele_list.append(index)
                ele_list.append(i.education)
                ele_list.append(i.leibie)
                ele_list.append(str(int(mon_wa_value)))
                ele_list.append(i.name)
                ele_list.append(i.work_area)
                ele_list.append(i.work_exp)
                ele_list.append(i.work_lable)
                data_list.append(ele_list)
                index+=1
            # if len(mon_walist)!=2:
            #     cot+=1
            #     print(i.mon_wa,i.name)
        # print(cot)
        self.list_to_hive(data_list=data_list,tablename='screen2')

    def leibiechuli(self):
        self.hive_context.sql('use dbzlzp')
        text_data = self.hive_context.sql('select * from screen2').collect()
        index=0
        data_list=[]
        for i in text_data:
            if str(i.leibie) in list1:
                continue
            elif str(i.leibie) in list2:
                if self.fenlei(str(i.name))=='web':
                    ele_list=[]
                    ele_list.append(index)
                    ele_list.append(i.education)
                    ele_list.append('WEB前端开发')
                    ele_list.append(i.mon_wa)
                    ele_list.append(i.name)
                    ele_list.append(i.work_area)
                    ele_list.append(i.work_exp)
                    ele_list.append(i.work_lable)
                    data_list.append(ele_list)
                    index+=1
                    continue
                elif self.fenlei(str(i.name))=='c':
                    ele_list=[]
                    ele_list.append(index)
                    ele_list.append(i.education)
                    ele_list.append('C语言开发工程师')
                    ele_list.append(i.mon_wa)
                    ele_list.append(i.name)
                    ele_list.append(i.work_area)
                    ele_list.append(i.work_exp)
                    ele_list.append(i.work_lable)
                    data_list.append(ele_list)
                    index+=1
                    continue
                elif self.fenlei(str(i.name))=='db':
                    ele_list=[]
                    ele_list.append(index)
                    ele_list.append(i.education)
                    ele_list.append('数据库管理员')
                    ele_list.append(i.mon_wa)
                    ele_list.append(i.name)
                    ele_list.append(i.work_area)
                    ele_list.append(i.work_exp)
                    ele_list.append(i.work_lable)
                    data_list.append(ele_list)
                    index+=1
                    continue
                elif self.fenlei(str(i.name))=='java':
                    ele_list = []
                    ele_list.append(index)
                    ele_list.append(i.education)
                    ele_list.append('Java开发工程师')
                    ele_list.append(i.mon_wa)
                    ele_list.append(i.name)
                    ele_list.append(i.work_area)
                    ele_list.append(i.work_exp)
                    ele_list.append(i.work_lable)
                    data_list.append(ele_list)
                    index += 1
                    continue
                elif self.fenlei(str(i.name))=='php':
                    ele_list = []
                    ele_list.append(index)
                    ele_list.append(i.education)
                    ele_list.append('PHP开发工程师')
                    ele_list.append(i.mon_wa)
                    ele_list.append(i.name)
                    ele_list.append(i.work_area)
                    ele_list.append(i.work_exp)
                    ele_list.append(i.work_lable)
                    data_list.append(ele_list)
                    index += 1
                    continue
                elif self.fenlei(str(i.name)) == 'bd':
                    ele_list = []
                    ele_list.append(index)
                    ele_list.append(i.education)
                    ele_list.append('大数据/人工智能')
                    ele_list.append(i.mon_wa)
                    ele_list.append(i.name)
                    ele_list.append(i.work_area)
                    ele_list.append(i.work_exp)
                    ele_list.append(i.work_lable)
                    data_list.append(ele_list)
                    index += 1
                    continue
                elif self.fenlei(str(i.name)) == 'qianru':
                    ele_list = []
                    ele_list.append(index)
                    ele_list.append(i.education)
                    ele_list.append('嵌入式软件开发')
                    ele_list.append(i.mon_wa)
                    ele_list.append(i.name)
                    ele_list.append(i.work_area)
                    ele_list.append(i.work_exp)
                    ele_list.append(i.work_lable)
                    data_list.append(ele_list)
                    index += 1
                    continue
                else:
                    continue
            else:
                ele_list = []
                ele_list.append(index)
                ele_list.append(i.education)
                ele_list.append(i.leibie)
                ele_list.append(i.mon_wa)
                ele_list.append(i.name)
                ele_list.append(i.work_area)
                ele_list.append(i.work_exp)
                ele_list.append(i.work_lable)
                data_list.append(ele_list)
                index += 1
                continue
        print(data_list)
        self.list_to_hive(data_list=data_list,tablename='screen3')

    def fenlei(self,str1):
        for j in web_list:
            if str(j) in str1.lower():
                return 'web'
            else:
                pass
        for j in C_list:
            if str(j) in str1.lower():
                return 'c'
            else:
                pass
        for j in db_list:
            if str(j) in str1.lower():
                return 'db'
            else:
                pass
        if 'java' in str1.lower():
            return 'java'
        if 'php' in str1.lower():
            return 'php'
        for j in bd_deeple:
            if str(j) in str1.lower():
                return 'bd'
            else:
                pass
        if '嵌入' in str1.lower():
            return 'qianru'

# app_list = ['app', ]
# C_list = ['c语言', 'c++', ]
# 数据库管理员_list = ['mysql', 'sql', '数据库', ]
# ruanjian_list = ['c#', '.net', 'python']
# java_list = ['java']
# php_list = ['php']
# bd_deeple = ['大数据', '人工智能', '深度学习', '']
# qianru_list = ['嵌入']
if __name__=='__main__':
    caozuo=CsvToHive()
    # list1=caozuo.read_csv_to_list(screen_e_file)
    # caozuo.list_to_hive(list1)
    # caozuo.select_hive_data('dbzlzp','screnn')
    caozuo.leibiechuli()

