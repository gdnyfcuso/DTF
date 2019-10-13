from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
import pandas as pd

def beginSpider():
    driver = webdriver.PhantomJS(executable_path=r"D:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    file_path=os.path.join(os.getcwd(),'fund_rest.txt')
    fund_code =pd.read_table(filepath_or_buffer=file_path,sep=',')
    Codes=fund_code.trade_code
    rownum = 1
    for Code in Codes:
        Code = str(Code).zfill(6)
        print (Code)
        fund_url='http://fund.eastmoney.com/f10/jjjz_'+Code +'.html'
        driver.get(fund_url) # 要抓取的网页地址
        try:
            tables = driver.find_element_by_class_name("bs_gl")
            for row in tables.find_elements_by_xpath("p"):
                col = row.find_elements(By.TAG_NAME, "label")
                try:
                    colum0 = col[0].text
                    colum1 = col[1].text
                    colum2 = col[2].text
                    colum3 = col[3].text
                    colum4 = col[4].text
                    colum0 = colum0.replace("成立日期：","")
                    colum1 = colum1.replace("基金经理：  ","")
                    colum2 = colum2.replace("类型：","")
                    colum3 = colum3.replace("管理人：","")
                    colum4 = colum4.replace("资产规模： ","")
                    colum4 = colum4.replace(",","")
                    colum4 = colum4.replace(",","")
                    with open('Leixingall.txt','ab') as files:
                        JJCD = str(rownum) +','+Code+','+colum0+','+colum1+','+colum2+','+colum3+','+colum4+ '\r\n'
                        JJCD = JJCD.encode('utf-8')
                        files.write(JJCD)
                        rownum += 1
                except:
                    pass
        except:
            pass
            time.sleep(0.1)
beginSpider()