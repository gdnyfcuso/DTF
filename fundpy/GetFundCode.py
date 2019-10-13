from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.PhantomJS(executable_path=r"D:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
driver.get("http://fund.eastmoney.com/allfund.html") # 要抓取的网页地址
tables = driver.find_element_by_id("code_content")
rownum = 1
for row in tables.find_elements_by_xpath(".//li"): 
    col = row.find_elements(By.TAG_NAME, "a")
    try:
        colum0 = col[0].text 
        colum0 = colum0.replace("（","")
        colum0 = colum0.replace("）",",")
        with open('JJCD.txt','ab') as files:
            JJCD = str(rownum) +','+colum0+ '\r\n'
            JJCD=JJCD.encode('utf-8')
            files.write(JJCD)
            rownum += 1
    except: 
        pass 