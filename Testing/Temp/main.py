import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

df = pd.read_csv('temp_data.csv', sep=',')
spw = 10
ishift = 5.88
print(list(df))

delay = 0

df['Amp_rolling'] = df[' Amp'].rolling(50, center=True, min_periods=1).mean().shift(-delay)
df['Shift_rolling'] = df[' Shift'].rolling(50, center=True, min_periods=1).mean().shift(-delay)


# Hs = amp*math.sin(math.pi*2*sft_out/spw)
# Hp = amp*math.cos(math.pi*2*sft_out/spw)

df[' Hs'] = df['Amp_rolling']*np.sin(math.pi*2*(df['Shift_rolling']-ishift)/spw)
df[' Hp '] = df['Amp_rolling']*np.cos(math.pi*2*(df['Shift_rolling']-ishift)/spw)

print(df.head())
print('-----')
print(df.tail())
cut_df = df.query('ID > 2400').query('ID < 7800')


plt.plot(cut_df['ID'], cut_df[' Temp']*1200 - 22000)
plt.plot(cut_df['ID'], cut_df[' Hs'])

plt.plot(cut_df['ID'], cut_df[' Hp ']*1.9-68000)
# plt.plot(cut_df['ID'], cut_df['Amp_rolling'])

# plt.scatter(cut_df[' Temp'], cut_df[' Hs'], s=0.5)

plt.xlabel("Temperature")
plt.legend()
plt.show()
