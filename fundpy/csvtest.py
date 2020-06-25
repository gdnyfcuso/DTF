# -*- coding:utf-8 -*-
############################################################################
import datetime
import os
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
    file_path=os.path.join(os.getcwd(),'fund.csv')
    fund_code = pd.read_csv(filepath_or_buffer=file_path, encoding='utf-8')
    print(len(fund_code))
    #HGZ= fund_code.loc[fund_code['name'].str.contains('债|货币|理财')==False,['trade_code']]  
    HGZ= fund_code.loc[fund_code['name'].str.contains('股票|指数|混合|联接')==True,['trade_code']]  
    print(len(HGZ))
    return HGZ
    #print ( Code)
    #print(fund_code)

if __name__ == "__main__":
    main()