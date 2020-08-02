# -*- coding:utf-8 -*-
# 在选定周期内任一历史时点往后推，产品净值走到最低点时的收益率回撤幅度的最大值。最大回撤用来描述买入产品后可能出现的最糟糕的情况。最大回撤是一个重要的风险指标，对于对冲基金和数量化策略交易，该指标比波动率还重要。
#D为某一天的净值，i为某一天，j为i后的某一天，Di为第i天的产品净值，Dj则是Di后面某一天的净值
#drawdown就是最大回撤率
#drawdown=max（Di-Dj）/Di，其实就是对每一个净值进行回撤率求值，然后找出最大的。
#
import numpy as np
import matplotlib.pyplot as plt

class RetracementRate:
    def MaxDrawdown(self,return_list):
           # '''最大回撤率'''
            i = np.argmax((np.maximum.accumulate(return_list) - return_list) / np.maximum.accumulate(return_list))  # 结束位置
            if i == 0:
                return 0
            j = np.argmax(return_list[:i])  # 开始位置
            return (return_list[j] - return_list[i]) / (return_list[j])
    def MaxDrawdownOneSelf(self,return_list):
        #"""最大回撤率"""
        maxac=np.zeros(len(return_list))
        b=return_list[0]
        for i in range(0,len(return_list)): #遍历数组，当其后一项大于前一项时，赋值给b
            if return_list[i]>b:
                b=return_list[i]
            maxac[i]=b
        print(maxac)
        i=np.argmax((maxac-return_list)/maxac) #结束位置
        if i == 0:
            return 0
        j = np.argmax(return_list[:i])  # 开始位置
        return (return_list[j] - return_list[i]) / (return_list[j])
 
def main():
    rr=RetracementRate()
    return_list=[12,12,21,15,27,16,21,22,25,20,16,17]
    print('MaxDrawdown')
    print(rr.MaxDrawdown(return_list))
    print("MaxDrawdownOneSelf")
    print(rr.MaxDrawdownOneSelf(return_list))
if __name__ == "__main__":
    main()