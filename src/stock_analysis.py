import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
from plotly.offline import iplot

from DbBase import DbBase
from utils.Alpha_code_101_1 import  Alphas, get_alpha
import seaborn as sns
from dao import db_utils
import matplotlib as matlab
from sklearn import preprocessing
from bubbly.bubbly import bubbleplot

daily_prime_col = ['open', 'close', 'pct_chg', 'vol', 'amount', 'change']
daily_view_prime_col = ['pre1_change', 'current_change', 'pre1_amount', 'current_amount', 'pre1_vol', 'current_vol']
comparing_alphas = []
for i in range(1, 10):
    comparing_alphas.append("alpha" + str(i).zfill(3))

query_factor = '300273.SZ'
# query_factor = '000011.SZ'
working_list = daily_prime_col #daily_prime_col + comparing_alphas


def time_change_amount_core(df_data):
    fig = plt.figure()
    ax = Axes3D(fig)
    df_data[daily_prime_col] = df_data[daily_prime_col] / df_data[daily_prime_col].max().astype(pd.np.float64)
    df_data['trade_data'] = df_data['trade_date'].astype("int")
    ax.plot(df_data['trade_date'], df_data['change'], df_data['amount'])
    plt.show()


def change_open_core(df):
    df_data = df
    df_data = df_data[daily_prime_col] / df_data[daily_prime_col].max().astype(pd.np.float64)
    sns.jointplot(x="open", y="change", data=df_data, color="purple")

    plt.show()


def change_amount_core(df):
    df_data = df
    df[daily_prime_col] = df_data[daily_prime_col] / df_data[daily_prime_col].max().astype(pd.np.float64)
    sns.jointplot(x="amount", y="change", data=df, color="purple")

    plt.show()


def pre1change_currchange_core(df):
    df_data = df
    df[daily_prime_col] = df_data[daily_view_prime_col] / df_data[daily_view_prime_col].max().astype(pd.np.float64)
    sns.jointplot(x="pre1_change", y="current_change", data=df, color="purple")
    plt.show()


def pre1vol_currchange_core(df):
    df_data = df
    df[daily_prime_col] = df_data[daily_prime_col] / df_data[daily_prime_col].max().astype(pd.np.float64)
    sns.jointplot(x="pre1_amount", y="current_change", data=df, color="purple")
    plt.show()





if __name__ == '__main__':
    # change_open_core(df_data)
    df_data = db_utils.get_daily_with_tmr_trade_data_by_tscode('000001.SZ')
    print("got data")
    pre1change_currchange_core(df_data)