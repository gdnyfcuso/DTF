from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from threading import Thread, Lock
import os
import time
from selenium.webdriver.common.by import By
import pandas as pd
# 下面是利用 selenium 抓取html页面的代码
# 初始化函数


def initSpider(fund_url, driver):
    driver.get(fund_url)  # 要抓取的网页地址
    # 找到"下一页"按钮,就可以得到它前面的一个label,就是总页数
    getPage_text = driver.find_element_by_id("pagebar").find_element_by_xpath(
        "div[@class='pagebtns']/label[text()='下一页']/preceding-sibling::label[1]").get_attribute("innerHTML")
    # 得到总共有多少页
    total_page = int("".join(filter(str.isdigit, getPage_text)))
    # 返回
    return total_page
# 获取html内容


def getData(myrange, driver, lock, code):
    for x in myrange:
        # 锁住
        lock.acquire()
        jjcode = code
        tonum = driver.find_element_by_id("pagebar").find_element_by_xpath(
            "div[@class='pagebtns']/input[@class='pnum']")
        # 得到 页码文本框
        jumpbtn = driver.find_element_by_id("pagebar").find_element_by_xpath(
            "div[@class='pagebtns']/input[@class='pgo']")
        # 跳转到按钮
        tonum.clear() # 第x页 输入框
        tonum.send_keys(str(x)) # 去第x页
        jumpbtn.click() # 点击按钮
        time.sleep(1)
        WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id("pagebar").find_element_by_xpath("div[@class='pagebtns']/label[@value={0} and @class='cur']".format(x)) != None)
        table = driver.find_element_by_xpath("//table[@class='w782 comm lsjz']/tbody")
        for row in table.find_elements_by_xpath(".//tr"):
            col = row.find_elements(By.TAG_NAME, "td")
            colum0 = col[0].text # 日期       
            colum1 = col[1].text # 当前价格
            colum1 = colum1.replace("*", "")
            colum2 = col[2].text # 总价格
            if colum2 == '':
                colum2 = colum1
            colum3 = col[3].text # 比率
            colum3 = colum3.replace("%", "")
            print(colum0)
            with open(jjcode+'.csv', 'ab') as files:
                items = jjcode + ','+colum0 + ',' + colum1 + ',' + colum2 + ',' + colum3 + '\r\n'
                items = items.encode('utf-8')
                files.write(items)
 # 解锁
        lock.release()
# 开始抓取函数
def beginSpider():
    file_path = os.path.join(os.getcwd(), 'JJCD.txt')


    fund_code = pd.read_table(filepath_or_buffer=file_path, sep=',')
    Codes = fund_code.trade_code
    driver = webdriver.PhantomJS(executable_path=r"D:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    for Code in Codes:
        Code = str(Code).zfill(6)
        print (Code)
        fund_url = 'http://fund.eastmoney.com/f10/jjjz_'+Code + '.html'
         # 初始化爬虫
        total_page = initSpider(fund_url, driver)
        # 创建锁
        lock = Lock()
        if total_page > 20:
            total_page = 20
        r = range(1, int(total_page)+1)
        step = 10
        # 把页码分段
        range_list = [r[x:x + step] for x in range(0, len(r), step)]
        thread_list = []
        for r in range_list:
            t = Thread(target=getData, args=(r, driver, lock, Code))
            thread_list.append(t)
            t.start()
        for t in thread_list:
            t.join()  # 这一步是需要的,等待线程全部执行完成   
        print('抓取完成 %s' % Code)
# #################上面代码就完成了 抓取远程网站html内容并保存到项目中的 过程   
beginSpider()