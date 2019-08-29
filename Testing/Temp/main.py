import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats

df = pd.read_csv('temp_data1.csv', sep=',')
spw = 10
ishift = 6.5
print(list(df))

delay = 0

df['Amp_rolling'] = df[' Amp'].rolling(100, center=True, min_periods=1).mean().shift(-delay)
df['Shift_rolling'] = df[' Shift'].rolling(100, center=True, min_periods=1).mean().shift(-delay)

df['Temp_rolling'] = df[' Temp'].rolling(200, center=True, min_periods=1).mean().shift(-delay)
# Hs = amp*math.sin(math.pi*2*sft_out/spw)
# Hp = amp*math.cos(math.pi*2*sft_out/spw)

df[' Hs'] = df['Amp_rolling']*np.sin(math.pi*2*(df['Shift_rolling']-ishift)/spw)
df[' Hp '] = df['Amp_rolling']*np.cos(math.pi*2*(df['Shift_rolling']-ishift)/spw)


print(df.head())
print('-----')
print(df.tail())
cut_df = df  # .query('ID > 2400').query('ID < 7800')
# cut_df = df.query('ID > 50').query('ID < 9500')

cut_df['Hs norm'] = cut_df[' Hs'] - cut_df[' Hs'].min()
cut_df['Hs norm'] = cut_df['Hs norm']/cut_df['Hs norm'].max()
# plt.plot(cut_df['ID'], cut_df['Hs norm'])


cut_df['Hp norm'] = cut_df[' Hp '] - cut_df[' Hp '].min()
cut_df['Hp norm'] = cut_df['Hp norm']/cut_df['Hp norm'].max()
# plt.plot(cut_df['ID'], cut_df['Hp norm'])


cut_df['Temp norm'] = cut_df['Temp_rolling'] - cut_df['Temp_rolling'].min()
cut_df['Temp norm'] = cut_df['Temp norm']/cut_df['Temp norm'].max()
# plt.plot(cut_df['ID'], cut_df['Temp norm'])


# plt.plot(cut_df['ID'], cut_df[' Hp '])
# plt.plot(cut_df['ID'], cut_df[' Hs'])
# plt.plot(cut_df['ID'], cut_df[' Voltage'])


x = cut_df[' Hs']
y = cut_df[' Hp ']
plt.plot(cut_df['ID'], x)
plt.plot(cut_df['ID'], y)

# plt.close()
# plt.scatter(x, y, s=0.5)


slope, intercept, r_value, p_value, std_err = stats.linregress(
    x, y)


plt.title('r2: ' + str(round(r_value, 3)))
plt.xlabel("Temperature")
plt.ylabel("Hs")
plt.legend()
plt.show()
