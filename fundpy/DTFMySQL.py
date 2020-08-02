# -*- coding:utf-8 -*-

import pymysql
import time



class PyMySQL:
    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    # 数据库初始化 mySQL._init_('localhost', 'root', 'lixz', 'invest')
    def _init_(self, host='localhost', user='root', passwd='lixz', db='invest',port=3306,charset='utf8'):
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

def main():
    global mySQL, sleep_time, isproxy, proxy, header
    mySQL = PyMySQL()
    mySQL._init_()
    funds=mySQL.getfundcodesFrommysql()
    print("将要计算的基金代码如下共有(%s)个："%(len(funds)))
 
if __name__ == "__main__":
    main()