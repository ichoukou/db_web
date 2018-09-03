from sqlalchemy import Column,create_engine,String,Integer,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine=create_engine('mysql+mysqlconnector://user:password@id:port/data_analysis')
Base=declarative_base()

class PSrank(Base):             #职位工资排名
    __tablename__='pos_sal_rank'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    salary=Column(Float)

class CSrank(Base):             #城市平均工资排名
    __tablename__='city_sal_rank'
    id=Column(Integer,primary_key=True)
    city=Column(String(100))
    salary=Column(Float)


class BCrank(Base):             #需求大数据人才城市排名
    __tablename__='bigdt_city_rank'
    id=Column(Integer,primary_key=True)
    city=Column(String(100))
    count=Column(Integer)


class BTrank(Base):             #需求大数据人才的行业排名
    __tablename__='bigdt_trade_rank'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    count=Column(Integer)

class ITCrank(Base):            #IT行业各职位需求排名
    __tablename__='IT_cot_rank'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    count=Column(Integer)


class BPrank(Base):             #受欢迎的大数据职位排名
    __tablename__='bigdt_pos_rank'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    count=Column(Integer)

class BCSrank(Base):            #大数据需求职位最多的城市的对应工资
    __tablename__='sp_bdc'
    id=Column(Integer,primary_key=True)
    name=Column(String(100))
    salary=Column(Float)
    count=Column(Integer)

class BPSrank(Base):
    __tablename__='sp_bps'
    id = Column(Integer,primary_key=True)
    name=Column(String(100))
    salary=Column(Float)
    count=Column(Integer)

if __name__=='__main__':
    Base.metadata.create_all(engine)