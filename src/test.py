from pandas import DataFrame
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df: DataFrame = pd.DataFrame([[1, 2, 3, 4, 5], [3, 3, 4, 56, 6]], columns=['cols', 'col2', 'col3', 'col4', 'col5'], index=['a', 'b'])


print(corr)
ax = sns.heatmap(
    df,
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)
plt.show()
