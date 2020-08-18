import datetime
from runtime.logger import Logger
from pandas import DataFrame
from sqlalchemy.exc import IntegrityError
from QueryBase import DbBase
from dao import db_utils
import pandas as pd
import tushare as ts
import traceback


class Spiders(DbBase):
    def __init__(self):
        self.logger = Logger.get_logger(logger_name=self.__class__.__name__)

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
                self.logger.error('failed to process: %s with error: %s' % (current_str, repr(traceback.extract_stack())))

    def get_daily(self, start_date = None):
        current_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        today_date = datetime.datetime.today()
        while current_date <= today_date:
            print ("Start date: %s" % current_date.strftime("%Y%m%d"))
            current_date = current_date + datetime.timedelta(days=1)
            current_str = current_date.strftime("%Y%m%d")

            df: DataFrame = self.pro.daily(ts_code='', start_date=current_str, end_date=current_str)
            df["trade_date_ts"] = pd.to_datetime(df["trade_date"])
            try:
                df.to_sql(con=self.engine, name="daily", if_exists="append", index=False, chunksize=4000, method="multi")
            except IntegrityError:
                self.logger.warn("duplicate key found when fetching daily data: %s" % current_str)

    def get_stock_basic(self):
        df: DataFrame = self.pro.stock_basic(exchange='', list_status='L',
                                            fields='ts_code,symbol,name,fullname,enname,area,industry,market,exchange,list_date,is_hs')
        df.to_sql(con=self.engine, name="stock_basic", if_exists="replace", index=False, chunksize=4000, method="multi")

    def get_today_ticks(self,):
        data: DataFrame = self.pro.stock_basic(exchange='', list_status='L',
                                               fields='ts_code,symbol,name,area,industry,list_date')

        if data is None:
            return

        for index, row in data.iterrows():
            _symbol = row['symbol']
            df: DataFrame = ts.get_today_ticks(_symbol, pause=.5)
            if df is None:
                self.logger.warn("failed to fetch ticks info for code %s" % _symbol)
                continue
            try:
                today_date = datetime.datetime.today().date()
                max_daily = db_utils.get_max_daily_ticks(_symbol, today_date.strftime('%Y-%m-%d'))
                max_time = max_daily.head(1)['max'].values[0]
                # the code of in the stock market
                df['code'] = _symbol
                # the date of this task
                df['date'] = today_date
                # the server time stamp including date, hour, min, secs
                df['server_ts'] = pd.to_datetime(today_date.strftime('%Y-%m-%d ') + df['time'])
                if max_time is not None:
                    # only insert the data with the latest time flag
                    df = df.loc[df['time'] > max_time]
                df.to_sql(con=self.engine, name='daily_ticks', if_exists='append', index=False, chunksize=2000, method="multi")
            except Exception:
                self.logger.error("failed to fetch ticks for code %s, error msg: %s" % (_symbol, repr(traceback.extract_stack())))

    def get_hist_data(self, start_date):
        start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        today_date = datetime.datetime.today()
        data:DataFrame = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        for index, row in data.iterrows():
            _symbol = row['symbol']
            df: DataFrame = ts.get_hist_data(_symbol, start=start_date.strftime("%Y-%m-%d"), end=today_date.strftime("%Y-%m-%d"))
            if df is not None:
                df['symbol'] = _symbol
                df['server_ts'] = pd.to_datetime(df.index)
                try:
                    df.to_sql(con=self.engine, name='hist_data', if_exists='append', index=False, chunksize=4000, method="multi")
                except IntegrityError:
                    self.logger.error("duplicate row, skipped")
                else:
                    self.logger.error("failed to fetch hist data for code: %s, with error: %s" % (_symbol, repr(traceback.extract_stack())))
            else:
                self.logger.error("failed to process hist_data: %s" % start_date.strftime("%Y-%m-%d"))

    def get_sina_dd(self):
        ts.get_sina_dd()

    def get_real_quotes(self):
        pass

    @staticmethod
    def get_real_time_quote():
        df = db_utils.get_stock_basics()



if __name__ == "__main__":
    sp = Spiders()
    # sp.get_today_ticks('600848')
    # sp.get_daily('20200601')
    # sp.get_daily_basic('20120101')
    # sp.get_hist_data('20200601')