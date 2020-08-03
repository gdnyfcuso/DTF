'''
Author: your name
Date: 2020-08-02 14:08:00
LastEditTime: 2020-08-03 10:58:43
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \fundpy\csvtest.py
'''
# -*- coding:utf-8 -*-
############################################################################
import datetime
import os,sys
import random
import re
import time

import pandas as pd
import pymysql
#############################################################################
import requests
from bs4 import BeautifulSoup


def main():
    #从csv文件中获取基金代码清单（可从wind或者其他财经网站导出）
    file_path=os.path.join(os.getcwd(),'JJCD.csv')
    fund_code = pd.read_csv(filepath_or_buffer=file_path, encoding='utf-8')
    
    print(len(fund_code))
    #HGZ= fund_code.loc[fund_code['name'].str.contains('债|货币|理财')==False,['trade_code']]  
    #HGZ= fund_code.loc[fund_code['name'].str.contains('股票|指数|混合|联接')==True,['trade_code','name']]  
    HGZ= fund_code.loc[fund_code['name'].str.contains('股票|指数|混合')==True,['trade_code','name']]  
    HGZ.set_index(["trade_code"], inplace=True)
    rss=sys.path[0]+ '\\funds\\'
    tocsvpath= rss+"GZHL.csv";
    fund_code=HGZ.drop_duplicates(subset=None, keep='first', inplace=False)
    fund_code.to_csv(tocsvpath,encoding='utf-8')
    print(len(fund_code))
    return fund_code
    #print ( Code)
    #print(fund_code)

if __name__ == "__main__":
    main()