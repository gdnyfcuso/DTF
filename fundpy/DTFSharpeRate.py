# -*- coding:utf-8 -*-

import numpy as np

class DTFSharpeRate:    
    def sharpRateOne(self,df):
        #print(df)
        df=preData(df)
        mm=np.mean(df['nav_chg_rate'])
        nn=df['nav_chg_rate'].std()
        ss=mm-0.01059015326852
        SR=ss/nn
        #print(SR)
        SR1=SR*math.sqrt(252)
        return SR1

    def sharpRateTwo(self,df):
        df=preData(df)
        df1 = df['nav_chg_rate'] - (4/252)
        return ((df1.mean() * math.sqrt(252))/df1.std())
    def dingTouSharpRate(self,df):
        print(df['盈亏'])
        df1 = df['盈亏'] - (0.04/252)
        return ((df1.mean() * math.sqrt(252))/df1.std())
    def sharpe_rate(self,rets,rfRate=0.04,ntim=252):
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
    def preData(self,df):        
        df['nav_chg_rate']=df['nav_chg_rate'].replace('%','',regex=True).apply(float)
        return df        