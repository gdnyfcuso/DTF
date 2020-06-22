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
from datetime import datetime

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
    def searchFundNavData(self, fund_code):
        try:
            sql = 'SELECT the_date,nav FROM invest.fund_nav where fund_code=%s order by the_date asc'%(fund_code)
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
            sql = 'SELECT fund_code FROM invest.fund_info where fund_type=\' 混合型\' or fund_type=\'股票指数\' or fund_type=\' 股票型\''
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
def fund_dingtou(df100,fundcode):
    c_rate=2.0/1000
    #start_date='2019-01-01'
    start_date=pd.to_datetime('2010-01-01',format='%Y-%m-%d') 
    #end_date='2020-02-28' 
    end_date=pd.to_datetime('2020-02-28',format='%Y-%m-%d')
    df11=df100.sort_index();
    df=df11[(df11.index>=start_date)&(df11.index<=end_date)]
    print(df)

    df['投入资金']=300;
    df['累计投入资金']=round(df['投入资金'].cumsum(),3)
    df['买入股票数量']=round(df['投入资金']*(1-c_rate)/df['close'],2)
    df['累计股票数量']=round(df['买入股票数量'].cumsum(),2)
    df['累计股票市值']=round(df['累计股票数量']*df['close'],2)

    df['平均股票成本']=round(df['累计投入资金']/df['累计股票市值'],2)
    df['盈亏']=round(df['累计股票市值']/df['累计投入资金']-1,2)
    df['盈亏多少钱']=round(df['累计股票市值']-df['累计投入资金'],2)

    print(df)

    cols=['close','累计投入资金','累计股票数量','累计股票市值','平均股票成本','盈亏','盈亏多少钱']
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
    df['累计股票市值'].plot();
    #plt.show();

    return df3;

def main():
    global mySQL, sleep_time, isproxy, proxy, header
    mySQL = PyMySQL()
    mySQL._init_('localhost', 'root', 'lixz', 'invest')
    isproxy = 0  # 如需要使用代理，改为1，并设置代理IP参数 proxy
    proxy = {"http": "http://110.37.84.147:8080", "https": "http://110.37.84.147:8080"}#这里需要替换成可用的代理IP
    sleep_time = 0.1
    #fundSpiders.getFundJbgk('000001')
    # funds=mySQL.getFundCodesFromCsv()
    funds=mySQL.getfundcodesFrommysql()
    cols1=['close','累计投入资金','累计股票数量','累计股票市值','平均股票成本','盈亏','盈亏多少钱','code']
    df5=pd.DataFrame([], columns=cols1);
    for fund in funds:
         try:
            res= mySQL.searchFundNavData(fund)
            # clos=['date','close']
            clos=[]

            pdlist=list(res);
            pd0=pd.DataFrame([],clos)
            df=pd0.append(pdlist)
            df.columns=['date','close']
            df.set_index(["date"], inplace=True)
            print(df)
            
            print('##################################')
            df1= fund_dingtou(df,str(fund[0]).zfill(6))
            df1['code']=str(fund[0]).zfill(6);
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
