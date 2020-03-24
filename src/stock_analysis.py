import pandas as pd
import matplotlib.pyplot as plt
from DbBase import DbBase
from utils.Alpha_code_101_1 import  Alphas, get_alpha
import seaborn as sns
import matplotlib as matlab
from sklearn import preprocessing


if __name__ == '__main__':
    df_data = pd.read_sql_query("select * from daily where ts_code='300273.SZ'", con=DbBase.engine)
    alp = Alphas(df_data)
    get_alpha(df_data)

    sns.scatterplot(df_data['alpha001'], df_data['change'])
    plt.show()



