import datetime
import traceback

from pandas import DataFrame
from src.DbBase import DbBase
import pandas as pd


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
                df.to_sql(con=self.engine, name="daily_basic", if_exists="append", index=False)
            except Exception:
                print(current_str)

    def get_daily(self, start_date = None):
        current_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        today_date = datetime.datetime.today()
        while current_date < today_date:
            current_date = current_date + datetime.timedelta(days=1)
            current_str = current_date.strftime("%Y%m%d")

            try:
                df: DataFrame = self.pro.daily(ts_code='', start_date=current_str, end_date=current_str)
                df["trade_date_ts"] = pd.to_datetime(df["trade_date"])
                df.to_sql(con=self.engine, name="daily", if_exists="append", index=False)
            except Exception:
                print(current_str)



if __name__ == "__main__":
    sp = Spiders()
    # sp.get_daily_basic("20190101")
    sp.get_daily("20190101")