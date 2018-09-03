import pandas as pd

def salary_cot(salstr):
    try:
        lower=salstr.split('-')[0]
        higher=salstr.split('-')[1]
        mean=float(lower)+float(higher)
        mean=mean/2
        return mean
    except:
        return salstr

df=pd.read_csv('./zp.csv',names=['bh','education','id','salary','name','city','work_desp','exp','lable'])
qt=df[:797414]
zl=df[797415:]
zl=zl.dropna()

zl['bh']=zl['bh'].apply(lambda i:int(i))
zl['id']=zl['id'].apply(lambda i:int(i))
# for i in zl['salary']:
#     print(type(i))
zl['city']=zl['city'].apply(lambda i:str(i).replace(',','|'))
zl['work_desp']=zl['work_desp'].apply(lambda i:str(i).replace(',','|').replace('\r','').replace('\n','').replace('\t',''))
zl['exp']=zl['exp'].apply(lambda i:str(i).replace(',','|'))
zl['lable']=zl['lable'].apply(lambda i:str(i).replace(',','|'))


zl['salary']=zl['salary'].apply(lambda i:salary_cot(i))
for i in zl['salary']:
    if type(i)==str:
        print(i)

for index,row in zl.iterrows():
    if type(row['salary'])==str:
        zl.drop(index,inplace=True)
print('处理完成')

zl['salary']=zl['salary'].apply(lambda i:salary_cot(i))

for i in zl['salary']:
    if type(i)==str:
        print(i)
# for i in zl:
#     print(i)
qt=qt.append(zl)
print(qt)
qt.to_csv('./zp2.csv')
