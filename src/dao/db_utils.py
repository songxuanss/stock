import pandas as pd

from DbBase import DbBase


def get_daily_by_tscode(ts_code):
    df_data = pd.read_sql_query("select * from daily where ts_code='%s'" % ts_code, con=DbBase.engine)
    return df_data

def get_daily_with_tmr_trade_data_by_tscode(ts_code):
    sql = """
        select * from daily_regression_1
    """

    return pd.read_sql_query(sql, con=DbBase.engine)

