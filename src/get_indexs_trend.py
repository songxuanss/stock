

from QueryBase import QueryBase
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl


mpl.rcParams['font.sans-serif'] = ['SimHei']


class indexs_info(QueryBase):
    def get_index_data(self, indexs):
        '''indexs是字典格式'''
        index_data={}
        for name,code in indexs.items():
            df=self.pro.index_daily(ts_code=code)
            df.index=pd.to_datetime(df.trade_date)
            index_data[name]=df.sort_index()
        return index_data


if __name__ == '__main__':
    #获取常见股票指数行情
    indexes={'上证综指': '000001.SH', '深证成指': '399001.SZ',
             '沪深300': '000300.SH','创业板指': '399006.SZ',
              '上证50': '000016.SH', '中证500': '000905.SH',
             '中小板指': '399005.SZ','上证180': '000010.SH'}
    idx_info = indexs_info()
    index_data=idx_info.get_index_data(indexes)
    #index_data['上证综指'].head()

    #对股价走势进行可视化分析
    subjects =list(index_data.keys())
    #每个子图的title
    plot_pos = [421,422,423,424,425,426,427,428] # 每个子图的位置
    new_colors = ['#1f77b4','#ff7f0e', '#2ca02c', '#d62728',
                 '#9467bd','#8c564b', '#e377c2',
                 '#7f7f7f','#bcbd22','#17becf']

    fig = plt.figure(figsize=(16,18))
    fig.suptitle('A market trend',fontsize=18)
    for pos in np.arange(len(plot_pos)):
        ax = fig.add_subplot(plot_pos[pos])
        y_data =index_data[subjects[pos]]['close']
        b = ax.plot(y_data,color=new_colors[pos])
        ax.set_title(subjects[pos])
        # 将右上边的两条边颜色设置为空，相当于抹掉这两条边
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
    plt.show()