#                                       简单说明

​                This is a fixed investment fund project, we can choose the best fund for you. We can get 10% return every year, so DTF will be your best fund tool!

特意说明：本程序只做研究使用，任何人不得将此程序用于商业目的，否则引起的一切法律问题与本程序作者无关！



安装mysql脚本 

​          [mysql 脚本]( fundpy\mysql)

下载数据模块：

​       [下载数据模块](DTFDataDown.py)

​        下载数据的数据源fundcode可以通过[所有代码](GetFundCode.py)模块下载并可以通过[筛选](csvtest.py)模块来选中自己需要的数据

运算模块：

​      [计算模块](DTFcalculate.py)

文件保存路径，默认为funds文件夹

每个代码都会以xxxD.csv命名（其中xxx代码基金代码或者股票代码），总文件会DD.CSV命名 每次写文件默认数据500条追加一次文件记录

​      数据量大概有500多万 查询如果没有做代化的话会比较慢



后续正在研究的内容

1.多因子买卖决策，来帮助我们真正的可以买到自己需要的

   主要包括的指标：1.时间 2.收益率3.加减金额的时机4.保证复利





















