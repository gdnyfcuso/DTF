# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import random
import pymysql
import os,sys
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import re
import math
import numpy as np
from datetime import datetime
from  Retracement import RetracementRate
from numpy import *

import annualVolatility as av

class PyMySQL:
    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    # 数据库初始化
    def _init_(self, host, user, passwd, db,port=3306,charset='utf8'):
        pymysql.install_as_MySQLdb()
        try:
            self.db =pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8')
            #self.db = pymysql.connect(ip, username, pwd, schema,port)
            self.db.ping(True)#使用mysql ping来检查连接,实现超时自动重新连接
            print (self.getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db)
            self.cur = self.db.cursor()
        except  Exception as e:
            print (self.getCurrentTime(), u"MySQL DB Connect Error :%d: %s" % (e.args[0], e.args[1]))
    # 插入数据
    def insertData(self, table, my_dict):
        try:
            #self.db.set_character_set('utf8')
            cols = ', '.join('%s' %id for id in my_dict.keys())
            ##values = '"," '.join(my_dict.values())
            values = '"," '.join('%s' %id for id in my_dict.values())
            
            sql = "replace into %s (%s) values (%s)" % (table, cols, '"' + values + '"')
            #print (sql)
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    #print (self.getCurrentTime(), u"Data Insert Sucess")
                    return insert_id
                else:
                    return 0
            except Exception as e:
                # 发生错误时回滚
                self.db.rollback()
                print (self.getCurrentTime(), u"Data Insert Failed: %s" % (e))
                return 0
        except Exception as e:
            print (self.getCurrentTime(), u"MySQLdb Error: %s" % (e))
            return 0
    def searchFundNavData(self, fund_code,startTime,endTime):
        try:
            sql = 'SELECT the_date,nav,nav_chg_rate FROM invest.fund_nav where nav_chg_rate is not null and nav_chg_rate <> \'\' and fund_code=%s and  the_date>\'%s\' and the_date<\'%s\' order by the_date asc'%(fund_code,startTime,endTime)
            #print (sql)
            try:
                self.cur.execute(sql)
                result= self.cur.fetchall()
                return result
                # 判断是否执行成功
            
            except Exception as e:
                # 发生错误时回滚
                print (self.getCurrentTime(), u"Data Select Failed: %s" % (e))
                return 0
        except Exception as e:
            print (self.getCurrentTime(), u"MySQLdb Error: %s" % (e))
            return 0
    def getfundcodesFrommysql(self):
        try:
            sql = 'SELECT fund_code FROM invest.fund_info where fund_type=\' 混合型\' or fund_type=\' 股票指数\' or fund_type=\' 联接基金\'  or fund_type=\' QDII\'  or fund_type=\' QDII-指数\' or fund_type=\' 股票型\''
            #print (sql)
            try:
                self.cur.execute(sql)
                result= self.cur.fetchall()
                return result
                # 判断是否执行成功
                
            except Exception as e:
                # 发生错误时回滚
                print (self.getCurrentTime(), u"Data Select Failed: %s" % (e))
                return 0
        except Exception as e:
            print (self.getCurrentTime(), u"MySQLdb Error: %s" % (e))
            return 0    
    def getFundCodesFromCsv(self):
        '''
        从csv文件中获取基金代码清单（可从wind或者其他财经网站导出）
        '''
        file_path=os.path.join(os.getcwd(),'fund_History.csv')
        fund_code = pd.read_csv(filepath_or_buffer=file_path, encoding='utf-8')
        Code=fund_code.trade_code
        #print ( Code)
        return Code
def getCurrentTime():
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))   
yRateList=[]
def cnav(fundlist,fundCode):
    dAmount=10
    dAmountList=[]
    dFenEList=[]
    yRate=0.0
    ztotalAmount=0.0
    zsy=0.0
    SyRate=0.0
    for myfund in fundlist:
        the_date=myfund[0]
        nav=myfund[1]
        dAmountList.append(dAmount)
        dFenEList.append(dAmount/nav)
        ztotalAmount=sum(dAmountList)
        totalFenAmount=sum(dFenEList)
        zsy=totalFenAmount*nav-ztotalAmount
        SyRate=zsy/ztotalAmount
        startTime=datetime.strptime(fundlist[0][0],' %Y-%m-%d')
        currentTime=datetime.strptime(the_date,' %Y-%m-%d')
        tS=(currentTime-startTime).total_seconds()
        print('##################################')

        if tS>0:
           years=round(tS/(365*24*60*60),5)
           if years>1:
              yRate=round((SyRate/years),4)*100
              print('年化收益：'+str(yRate)+'%')
        print('当前市值:'+str(round(totalFenAmount*nav,2)))
        print('总期数:'+str(len(dAmountList)))
        print('基金代码：'+fundCode)
        print('当前时间：'+the_date+'\n净值：'+str(nav)+"\n总投入："+str(ztotalAmount)+"\n总收益："+str(round(zsy,4))+"\n总收益率："+str(round(SyRate*100,4))+"%")
        print('##################################')
    if yRate>0.0:
       yRateList.append((yRate,fundCode,str(ztotalAmount),str(round(zsy,4)),str(round(SyRate*100,4))))

def fund_dingtou(df100,fundcode,initAmount=300,startTime='2016-01-01',endTime='2020-06-28'):
    c_rate=2.0/1000
    #start_date='2019-01-01'
    start_date=pd.to_datetime(startTime,format='%Y-%m-%d') 
    #end_date='2020-02-28' 
    end_date=pd.to_datetime(endTime,format='%Y-%m-%d')
    df11=df100.sort_index();
    df=df11[(df11.index>=start_date)&(df11.index<=end_date)]
    print(df)

    df['投入资金']=initAmount;
    df['累计投入资金']=round(df['投入资金'].cumsum(),5)
    df['买入基金份额']=round(df['投入资金']*(1-c_rate)/df['close'],5)
    df['累计基金份额']=round(df['买入基金份额'].cumsum(),5)
    df['累计基金市值']=round(df['累计基金份额']*df['close'],5)

    df['平均基金成本']=round(df['累计投入资金']/df['累计基金市值'],5)
    df['盈亏']=round(df['累计基金市值']/df['累计投入资金']-1,5)
    df['盈亏多少钱']=round(df['累计基金市值']-df['累计投入资金'],5)
    df['定投夏普比率']=''

    print(df)

    cols=['close','累计投入资金','累计基金份额','累计基金市值','平均基金成本','盈亏','盈亏多少钱']
    df=df[cols]

    print(df)

    rss=sys.path[0]+ '\\funds\\'
    tocsvpath= rss+fundcode+"D.csv";

    df.to_csv(tocsvpath,encoding='gbk')

    df0= df.sort_values(by=['盈亏'])
    df1=df0[-1:]
    print(df0)
    print(df1)


    df2= df0.sort_values(by=['盈亏多少钱'])
    df3=df2[-1:]
    print(df3)

    mpl.style.use('seaborn-whitegrid');

    df['盈亏多少钱'].plot();

    #plt.show()
    df['累计投入资金'].plot();
    df['累计基金市值'].plot();
    #plt.show();
    return df3;
def sharpRateOne(df):
    #print(df)
    df=preData(df)
    mm=np.mean(df['nav_chg_rate'])
    nn=df['nav_chg_rate'].std()
    ss=mm-0.01059015326852
    SR=ss/nn
    #print(SR)
    SR1=SR*math.sqrt(252)
    return SR1

def sharpRateTwo(df):
    df=preData(df)
    df1 = df['nav_chg_rate'] - (4/252)
    return ((df1.mean() * math.sqrt(252))/df1.std())
def dingTouSharpRate(df):
    print(df['盈亏'])
    df1 = df['盈亏'] - (0.04/252)
    return ((df1.mean() * math.sqrt(252))/df1.std())
def sharpe_rate(rets,rfRate=0.04,ntim=252):
    '''
    sharpe_rate(rets,rfRate,ntim=252):
        计算夏普指数
    【输入】
    	rets (list): 收盘价（一天一条）
      rfRate (int): 无风险收益利润
      ntim (int): 交易时间（按天、小时、等计数）
         采用小时(60分钟)线数据，ntim= 252* 6.5 = 1638.
    【输出】
        夏普指数数值
        '''
    rsharp= 0.0
    if len(rets):
        returns = diff(rets)/rets[:-1]
        rstd =returns.std(ddof=1) #np.stddev(rets, 1)  #收益波动率
        print('标准差%s'%(rstd))
        if rstd != 0:
            rfPerRet = rfRate / float(ntim)
            rmean=returns.mean()
            avgExRet = rmean - rfPerRet
            dsharp = avgExRet / rstd
            rsharp = dsharp * np.sqrt(ntim)
    return rsharp



#这里的收益率不要除以100 4.5的意思 就是4.5%=0.045 如果收益率除以100 夏普比率的计算也要除以100
def preData(df):        
    df['nav_chg_rate']=df['nav_chg_rate'].replace('%','',regex=True).apply(float)
    return df

def main():
    global mySQL, sleep_time, isproxy, proxy, header
    mySQL = PyMySQL()
    mySQL._init_('localhost', 'root', 'lixz', 'invest')
    isproxy = 0  # 如需要使用代理，改为1，并设置代理IP参数 proxy
    proxy = {"http": "http://110.37.84.147:8080", "https": "http://110.37.84.147:8080"}#这里需要替换成可用的代理IP
    sleep_time = 0.1
    maxDownRate=RetracementRate()
    funds=mySQL.getfundcodesFrommysql()
    print("将要计算的基本代码如下：")
    print(funds)
    cols1=['close','累计投入资金','累计基金份额','累计基金市值','平均基金成本','盈亏','盈亏多少钱','code','夏普比率','夏普比率(重新计算)','最大回撤率','标准差','定投天数','年波动率','年化收益率','月波动率']
    df5=pd.DataFrame([], columns=cols1);
    startTime='2018-01-01'
    endTime='2050-06-28'
    for fund in funds:
         try:
            res= mySQL.searchFundNavData(fund[0],startTime,endTime)
            # clos=['date','close']
            clos=[]
            pdlist=list(res);
            pd0=pd.DataFrame([],clos)
            df=pd0.append(pdlist)
            df.columns=['date','close','nav_chg_rate']
            df.set_index(["date"], inplace=True)
            print(df)
            
            print('##################################')
            df1= fund_dingtou(df,str(fund[0]).zfill(6),startTime=startTime,endTime=endTime)
            df1['code']=str(fund[0]).zfill(6);
            df1['夏普比率']=sharpRateTwo(df)
            df1['夏普比率(重新计算)']=sharpe_rate(list(df['close']))
            df1['标准差']=df['nav_chg_rate'].std()/100
            df1['最大回撤率']=maxDownRate.MaxDrawdown(df['close'])
            df1['定投天数']=len(df)
            dingcount=(df1['定投天数']/252)
            df1['年波动率']=av.annualVolatilityYear(list(df['close']))
            df1['月波动率']=df1['年波动率']*sqrt(1/12)
            df1['年化收益率']=df1['盈亏']/dingcount
            print(df1)
            df5=df5.append(df1[0:]);
            print('##################################')
         except Exception as e:
            print (getCurrentTime(),'main', fund,e )
    print(df5);
    # rss=sys.path[0]+ '\\zwdat\\cn\\day_D\\' 
    rss=sys.path[0]+ '\\funds\\'
    tocsvpath= rss+"DD.csv";

    df5.to_csv(tocsvpath,encoding='gbk')
    
    # content= sorted(yRateList,reverse=False)
    # with open('test.txt','a') as file_test:
    #     file_test.write(str(content))
    # print(content)
 
if __name__ == "__main__":
    main()
