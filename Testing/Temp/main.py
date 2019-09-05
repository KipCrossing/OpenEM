import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats

df = pd.read_csv('temp_data_cobbity2.csv', sep=',')
spw = 10
ishift = 7.5
# temprature vector at 7.1 and
# the Change vector at 6.85 +- 2.5

print(list(df))

delay = 0

roll = 20

df['Temp_rolling'] = df[' Temp'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
# Hs = amp*math.sin(math.pi*2*sft_out/spw)
# Hp = amp*math.cos(math.pi*2*sft_out/spw)

df[' Hs'] = df[' Amp']*np.sin(math.pi*2*(df[' Shift']-ishift)/spw)
df[' Hp '] = df[' Amp']*np.cos(math.pi*2*(df[' Shift']-ishift)/spw)

df['Amp_rolling'] = df[' Amp'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
df['Hs_rolling'] = df[' Hs'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
df['Hp_rolling'] = df[' Hp '].rolling(roll, center=True, min_periods=1).mean().shift(-delay)

df['Volt_rolling'] = df[' Voltage'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)


print(df.head())
print('-----')
print(df.tail())
cut_df = df  # .query('ID > 0').query('ID < 17000')
# cut_df = df.query('ID > 50').query('ID < 9500')

cut_df['Hs norm'] = cut_df['Hs_rolling'] - cut_df['Hs_rolling'].min()
cut_df['Hs norm'] = cut_df['Hs norm']/cut_df['Hs norm'].max()
# plt.plot(cut_df['ID'], cut_df['Hs norm'])


cut_df['Hp norm'] = cut_df['Hp_rolling'] - cut_df['Hp_rolling'].min()
cut_df['Hp norm'] = cut_df['Hp norm']/cut_df['Hp norm'].max()
# plt.plot(cut_df['ID'], cut_df['Hp norm'])


cut_df['Temp norm'] = cut_df['Temp_rolling'] - cut_df['Temp_rolling'].min()
cut_df['Temp norm'] = cut_df['Temp norm']/cut_df['Temp norm'].max()
# plt.plot(cut_df['ID'], cut_df['Temp norm'])


cut_df['Amp norm'] = cut_df['Amp_rolling'] - cut_df['Amp_rolling'].min()
cut_df['Amp norm'] = cut_df['Amp norm']/cut_df['Amp norm'].max()
# plt.plot(cut_df['ID'], cut_df['Amp norm'])


x = cut_df['Temp norm']
y = cut_df['Hs norm']

plt.plot()
plt.plot(cut_df['ID'], x)
plt.plot(cut_df['ID'], y)
plt.show(block=True)

slope, intercept, r_value, p_value, std_err = stats.linregress(
    x, y)
plt.scatter(x, y, s=0.5)
plt.xlabel("Temp")
plt.ylabel("Hs")
plt.title('r2: ' + str(round(r_value, 3))+'\nShift = ' + str(round(ishift/10, 3)))
plt.show(block=True)


plt.subplot(4, 1, 1)
plt.plot(cut_df['ID'], cut_df['Hp_rolling'], c='r')
plt.title('r2: ' + str(round(r_value, 3))+'\nShift = ' + str(round(ishift/10, 3)))
plt.ylabel("Hp")
plt.subplot(4, 1, 2)
plt.plot(cut_df['ID'], cut_df['Hs_rolling'])
plt.ylabel("Hs")
plt.subplot(4, 1, 3)
plt.plot(cut_df['ID'], cut_df['Temp_rolling'], c='g')
plt.ylabel("Temp")
plt.subplot(4, 1, 4)
plt.plot(cut_df['ID'], cut_df['Volt_rolling'], c='purple')
plt.ylabel("Voltage")


plt.xlabel("Time")

# plt.legend()
plt.show(block=True)
