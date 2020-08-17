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
from DTFMySQL import PyMySQL
from DTFSharpeRate import DTFSharpeRate

class DTFcalculate:

    def __init__(self):
        pass
    
    def fund_dingtou(self,df100,fundcode,initAmount=300,startTime='2016-01-01',endTime='2020-06-28'):
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


def main():
    global mySQL, sleep_time, isproxy, proxy, header,dtfSharpeRate
    mySQL =PyMySQL()
    dtfcore=DTFcalculate()
    
    dtfSharpeRate=DTFSharpeRate()
    mySQL._init_('localhost', 'root', 'lixz', 'invest')
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
            
            df1=dtfcore.fund_dingtou(df,str(fund[0]).zfill(6),startTime=startTime,endTime=endTime)
            df1['code']=str(fund[0]).zfill(6);
            df1['夏普比率']=dtfSharpeRate.sharpRateTwo(df)
            df1['夏普比率(重新计算)']=dtfSharpeRate.sharpe_rate(list(df['close']))
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
if __name__ == "__main__":
    main()
