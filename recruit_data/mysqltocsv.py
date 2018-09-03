import pandas as pd
from sqlalchemy import Column,create_engine,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
start=time.time()
Base=declarative_base()
def shaixuan(list1,str1):
    for i in list1:
        if i in str1:
            return False
        else:
            continue
    return True


class zlzp(Base):
    __tablename__='zlzp1'
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    mon_wa=Column(String(20))
    education=Column(String(20))
    work_exp=Column(String(20))
    leibie=Column(String(50))
    work_area=Column(String(20))
    work_lable=Column(String(100))
    work_desp=Column(String(10000))

class qtzp(Base):
    __tablename__='qtzp'
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    mon_wa=Column(String(20))
    education=Column(String(20))
    work_exp=Column(String(20))
    work_area=Column(String(20))
    work_lable=Column(String(100))
    work_desp=Column(String(10000))

engine=create_engine('mysql+mysqlconnector://user:pswd@ip:port/zp')

list=['销售', '美工', '商务', '经理', '网店', '客服', '文员', '行政', '辅导', '总监', '讲师', '淘宝', '运营', '渠道', '支持', '市场',
      '文案', '财务', '前台', '人事', '主管', '店长', '管家', '专员', '海运', '人力', '业务', '网销', '咨询', '助理', '摄影', '房产',
      '平面', '产品', '报价', '课程', '视觉', '管理', '动漫', '动画', '顾问', '维修', '老师', '幼师', '干部', '司机', '策划', '制图',
      '营销', '出纳', '投资', '建筑', '信用', '库管', '执行', '股票', '操盘', '理财', '活动', '评估', '资金', '机械', '拍摄', '储备',
      '信贷', '专利', '会计', '编辑', '视频', '造价', '法律', '顾问', '林业', '电话', '售', '儿童', '插画', '统计', '天猫', '车', '猎头',
      '招商', '店', '测量', '美容', '单', '调度', '话务', '合伙', '技工', '贸', '药', '代表', '经纪', '推广', '客户', '社', '公关', '挑战',
      '医', '女', '男', '剪辑', '买', '记者', '销', '秘书', '服装', '购', '图', '师', '漫', '画', '集团', '商标', '保险', '广告', '兼职',
      '购', '交易', '风', '贷', '翻译', '仓库', '内勤', '暑假', '钣金', '管培', '美术', '软文', '法务', '竞价', '美', '收银', '空调', '食堂',
      '分拣', '健身', '施工', '录入', '创业', '配送', '质检', '种植', '校长', '护士', 'logo', '出差', '操作', '学管', '货代', '厨', '教务',
      '英语', '播', '教学', '供应', '艺人', '电工', '打印机', '校', '助教', '督导', '主持', '生产', '发酵', '私人', '后勤',
      '土木','卫生','调查','热线','号码','包装','文职','机票','政策','保洁','生物','仓管','影视','班主任','钟点','办公','夏季','教研',
      '杂志','定损','物流','呼叫','监管','接线','主任','梦想','院长','网红','焊工','负责人','家装','催收','营业','选题','检测','理货',
      '水，电','媒介','中介','考试','化验','绿化','客管','寻访','测评','幼儿','钳工','品控','厂长','驾驶','导演','西班牙','园林',
      '房东','网球','足球','篮球','乒乓','体育','保安','排版','保研','录音','普工']

DBSession=sessionmaker(bind=engine)
session=DBSession()
# many_info=session.query(qtzp).all()
many_info=session.query(qtzp).all()
id=[]
name=[]
mon_wa=[]
education=[]
work_exp=[]
leibie=[]
work_area=[]
work_lable=[]
work_desp=[]
i=int(0)
# zpinfo=open('/home/hadoop/zlzp.txt','w')
# many_info=[]
# text=open('/home/hadoop/zlzp.txt','r')
# while True:
#     row=text.readline()
#     if row=='':
#         break
#     else:
#         many_info.append(row)
for info in many_info:
    # if shaixuan(list,info.name)==False:
    #     continue
    # else:
    id.append(info.id)
    name.append(info.name.replace(',','|'))
    mon_wa.append(info.mon_wa)
    education.append(info.education)
    work_exp.append(info.work_exp)
    work_area.append(info.work_area)
    work_lable.append(info.work_lable.replace(',','|'))
    work_desp.append(info.work_desp.replace(',','|'))
    print(info.name)
    i+=1
many_info=session.query(zlzp).all()
# print(i)
# print(len(list))
for info in many_info:
    id.append(info.id)
    name.append(info.name.replace(',','|'))
    mon_wa.append(info.mon_wa)
    education.append(info.education)
    work_exp.append(info.work_exp)
    work_area.append(info.work_area)
    work_lable.append(info.leibie.replace(',','|'))
    work_desp.append(info.work_desp.replace(',','|'))
session.close()
# zpinfo.close()
info_dict={
    'id':id,
    'name':name,
    'mon_wa':mon_wa,
    'education':education,
    'work_exp':work_exp,
    'work_area':work_area,
    'work_lable':work_lable,
    'work_desp':work_desp
}

info_df=pd.DataFrame(info_dict)
print(info_df)
info_df.to_csv('./zp.csv')
end=time.time()
print('所用时间：'+str(end-start)+'s')