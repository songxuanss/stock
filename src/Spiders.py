import datetime
import traceback
from pandas import DataFrame

from dao import db_utils
from src.DbBase import DbBase
import pandas as pd
import tushare as ts


class Spiders(DbBase):
    def __init__(self):
        pass

    def get_daily_basic(self, start_date=None):
        """
        :param start_date: in for format of YYYYMMDD: e.g: 20180101
        :return:
        """
        current_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        today_date = datetime.datetime.today()
        while current_date < today_date:
            current_date = current_date + datetime.timedelta(days=1)
            current_str = current_date.strftime("%Y%m%d")
            try:
                df: DataFrame = self.pro.daily_basic(ts_code='', trade_date=current_str,
                                                     fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,ps,dv_ratio,total_share,float_share,total_mv')
                df["trade_date_ts"] = pd.to_datetime(df["trade_date"])
                df.to_sql(con=self.engine, name="daily_basic", if_exists="append", index=False, chunksize=4000, method="multi")
            except Exception:
                print(current_str)

    def get_daily(self, start_date = None):
        current_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        today_date = datetime.datetime.today()
        today_str = today_date.strftime("%Y%m%d")
        # while current_date < today_date:
        # current_date = current_date + datetime.timedelta(days=1)
        current_str = current_date.strftime("%Y%m%d")

        try:
            df: DataFrame = self.pro.daily(ts_code='', start_date=current_str, end_date=today_str)
            df["trade_date_ts"] = pd.to_datetime(df["trade_date"])
            df.to_sql(con=self.engine, name="daily", if_exists="append", index=False, chunksize=4000, method="multi")
        except Exception:
            print(current_str)

    def get_stock_basic(self):
        df: DataFrame = self.pro.stock_basic(exchange='', list_status='L',
                                            fields='ts_code,symbol,name,fullname,enname,area,industry,market,exchange,list_date,is_hs')
        df.to_sql(con=self.engine, name="stock_basic", if_exists="replace", index=False, chunksize=4000, method="multi")

    def get_today_ticks(self, code):
        df: DataFrame = ts.get_today_ticks(code, pause=.5)
        today_date = datetime.datetime.today().date()
        max_daily = db_utils.get_max_daily_ticks(code, today_date.strftime('%Y-%m-%d'))
        max_time = max_daily.head(1)['max'].values[0]
        # the code of in the stock market
        df['code'] = code
        # the date of this task
        df['date'] = today_date
        # the server time stamp including date, hour, min, secs
        df['server_ts'] = pd.to_datetime(today_date.strftime('%Y-%m-%d ') + df['time'])
        if max_time is not None:
            # only insert the data with the latest time flag
            df = df.loc[df['time'] > max_time]
        df.to_sql(con=self.engine, name='ticks', if_exists='append', index=False, chunksize=2000, method="multi")

    @staticmethod
    def get_real_time_quote(code):
        df = db_utils.get_stock_basics()



if __name__ == "__main__":
    sp = Spiders()
    # sp.get_today_ticks('600848')
    sp.get_daily('20200403')
    sp.get_daily_basic('20200403')