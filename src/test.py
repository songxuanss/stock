from pandas import DataFrame
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df: DataFrame = pd.DataFrame([[1, 2, 3, 4, 5], [3, 3, 4, 56, 6]], columns=['cols', 'col2', 'col3', 'col4', 'col5'], index=['a', 'b'])
sns.scatterplot(df['cols'], df['col2'])
plt.show()
