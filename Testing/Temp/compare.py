import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('temp_data4.csv')

df = df  # .query('ID < 800')


slope, intercept, r_value, p_value, std_err = stats.linregress(
    df['Temp_rolling'], df['Amp_rolling'])
print('Slope: ', slope)
print('Intercept: ', intercept)
print('R value: ', r_value)

plt.scatter(df['Temp_rolling'], df['Amp'], s=0.5)

plt.show()


col = 'Amp'
print(df[col].describe())
print(df[col].describe())

print('-----------')
print(df[col].describe()['max'] - df[col].describe()['min'])
print(df[col].describe()['max'] - df[col].describe()['min'])
