from datetime import datetime
from multiprocessing.pool import ThreadPool

from pandas import DataFrame
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# df: DataFrame = pd.DataFrame([[1, 2, 3, 4, 5], [3, 3, 4, 56, 6]], columns=['cols', 'col2', 'col3', 'col4', 'col5'], index=['a', 'b'])
#
# import matplotlib
# print(matplotlib.matplotlib_fname())
# ax = sns.heatmap(
#     df,
#     vmin=-1, vmax=1, center=0,
#     cmap=sns.diverging_palette(20, 220, n=200),
#     square=True
# )
# ax.set_xticklabels(
#     ax.get_xticklabels(),
#     rotation=45,
#     horizontalalignment='right'
# )
# plt.show()

# print(datetime.today().date().strftime('%Y-%m-%d'))
from dao import db_utils

# db = db_utils.get_max_daily_ticks('000001','2020-04-07')
# max_date = db.head(1)['max'].values[0]
# print(max_date)


# time1='19:20:02'
#
# time2='09:30:03'
#
# time3 = '01:29:03'
# print(time3>time2)

# class x:
#
#     def __init__(self, x1, x2, x3, x4):
#         self.x1 = x1
#         self.x2 = x2
#         self.x3 = x3
#         self.x4 = x4
#
#     def y(self,x11,x12):
#         print(vars(self).items())
#         print(x.y.__code__.co_varnames)
#         print(hasattr(self, "x11"))
#
#
# if __name__ == '__main__':
#     xx = x(1,2,3,4)
#     xx.y(1, 2)


import tushare as ts

class QueryBase:
    ts.set_token('028572c95ef3d09342d099f2a44c61425d4b0ee0e7cbbff00104ba70')
    pro = ts.pro_api()

    def test(self):
        # f: DataFrame = self.pro.daily(trade_date='20190601')
        # f = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
        # f:DataFrame = ts.get_hist_data('000021', start='2020-01-05', end='2020-06-05')
        # df: DataFrame = ts.get_hist_data('000001', start='2019-01-01', end='2019-03-21')
        df:DataFrame = ts.get_today_ticks()

        df: DataFrame = ts.get_tick_data('600848', date='2020-06-09')
        print(df.to_string())


if __name__ == '__main__':
    c = QueryBase()
    c.test()