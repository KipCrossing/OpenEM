import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

am_df = pd.read_csv('Cobbity9_run'+str(1)+'.csv', sep=',')
pm_df = pd.read_csv('Cobbity9_run'+str(2)+'.csv', sep=',')
cal_am = am_df.query('ID < 2600')
cal_pm = pm_df.query('ID < 700')

am_df = am_df.query('ID > 4100').query('ID < 5000')
pm_df = pm_df.query('ID > 900').query('ID < 2000')

print(am_df.head())

# plt.scatter(am_df['Temp_rolling'], am_df['Sft_rolling'], s=0.5)
# plt.scatter(pm_df['Temp_rolling'], pm_df['Sft_rolling'], s=0.5)
# plt.show()

plt.scatter(cal_am['Temp_rolling'], cal_am['Shift'], s=0.5)
plt.scatter(cal_pm['Temp_rolling'], cal_pm['Shift'], s=0.5)
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(
    cal_am['Temp_rolling'], cal_am['Amp_rolling'])
print('Slope: ', slope)
print('Intercept: ', intercept)
print('R value: ', r_value)

# plt.scatter(cal_am['Temp_rolling'], cal_am['Amp'], s=0.5)
# plt.scatter(cal_pm['Temp_rolling'], cal_pm['Amp'], s=0.5)
# plt.show()


col = 'Amp'
print(cal_am[col].describe())
print(cal_pm[col].describe())

print('-----------')
print(am_df[col].describe()['max'] - am_df[col].describe()['min'])
print(pm_df[col].describe()['max'] - pm_df[col].describe()['min'])

# print(am_df[col].describe()['mean'])
# print(pm_df[col].describe()['mean'])
# print('-----------')
# print(am_df[col].describe()['mean']/cal_am[col].describe()['mean'],
#       pm_df[col].describe()['mean'] / cal_pm[col].describe()['mean'])
