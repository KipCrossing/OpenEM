import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats
import random

file_number = 2

df = pd.read_csv('temp_data_cobbity'+str(file_number)+'.csv', sep=',')
notes_df = pd.read_csv('temp_notes_cobbity'+str(file_number)+'.csv', sep=',')


spw = 10
ishift = 8.6  # - 0.375
# temprature vector at 7.1 and
# the Change vector at 6.85 +- 2.5

print(list(df))

delay = 0

roll = 20

df['Temp_rolling'] = df['Temp'].rolling(roll*100, center=True, min_periods=1).mean().shift(-delay)

# Hs = amp*math.sin(math.pi*2*sft_out/spw)
# Hp = amp*math.cos(math.pi*2*sft_out/spw)

df['Hs'] = df['Amp']*np.sin(math.pi*2*(df['Shift']-ishift)/spw)
df['Hp'] = df['Amp']*np.cos(math.pi*2*(df['Shift']-ishift)/spw)

df['Amp_rolling'] = df['Amp'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
df['Hs_rolling'] = df['Hs'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
df['Hp_rolling'] = df['Hp'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
df['Sft_rolling'] = df['Shift'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
df['Volt_rolling'] = df['Voltage'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)


print(df.head())
print('-----')
print(df.tail())
cut_df = df  # .query('ID > 7900').query('ID < 13400')

x = cut_df['Amp_rolling']
y = cut_df['Sft_rolling']

# plt.plot()
# plt.plot(cut_df['ID'], x*0.8)
# plt.plot(cut_df['ID'], y)
# plt.plot(cut_df['ID'], cut_df['Shift']/10)
#
# for rown in range(notes_df.shape[0]-1):
#     plt.axvline(x=notes_df.iloc[rown][0], color='black', ls='--', label=notes_df.iloc[rown][1])
#     plt.annotate(notes_df.iloc[rown][1], xy=(notes_df.iloc[rown][0], random.random()))
#
#
# plt.show(block=True)
#
slope, intercept, r_value, p_value, std_err = stats.linregress(
    x, y)
print('Slope: ', slope)
print('Intercept: ', intercept)
print('R value: ', r_value)
cut_df['Tem_Adj'] = (cut_df['Temp_rolling']*slope + intercept)
cut_df['Adj'] = cut_df['Sft_rolling'] - (cut_df['Temp_rolling']*slope + intercept)


df['Hs'] = df['Amp']*np.sin(math.pi*2*(cut_df['Adj']-ishift)/spw)
df['Hp'] = df['Amp']*np.cos(math.pi*2*(cut_df['Adj']-ishift)/spw)
df['Hs_rolling'] = df['Hs'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)
df['Hp_rolling'] = df['Hp'].rolling(roll, center=True, min_periods=1).mean().shift(-delay)

# Real/Imagionary
# plt.scatter(cut_df['Temp_rolling'], cut_df['Adj'], s=0.5)
# plt.scatter(cut_df['Temp_rolling'], cut_df['Sft_rolling'], s=0.5)
# plt.scatter(cut_df['Temp_rolling'], cut_df['Tem_Adj'], s=0.5)
# plt.legend()
# plt.show(block=True)

# cut_df['Ht_adj'] = (cut_df['Adj']**2 + cut_df['Hp_rolling']**2)**0.5
# cut_df['Sft_adj'] = np.arctan(cut_df['Adj']/cut_df['Hp_rolling'])purple


# plt.plot(cut_df['ID'], cut_df['Sft_rolling'])
# plt.plot(cut_df['ID'], cut_df['Tem_Adj'])
# plt.legend()
# plt.show()
#
# plt.plot(cut_df['ID'], cut_df['Adj'])
# plt.show()

to_plot = [['Amp_rolling', 'Amp_rolling', 'orange'], ['Hp_rolling', 'Hp', 'r'], [
    'Hs_rolling', 'Hs', 'b'], ['Temp_rolling', 'Temp', 'g'], ['Sft_rolling', 'Shift', 'purple'], ['Volt_rolling', 'Volt_rolling', 'yellow']]

# plt.subplot(len(to_plot), 1, 1)

for info_i in range(len(to_plot)):
    plt.subplot(len(to_plot), 1, info_i+1)
    plt.plot(cut_df['ID'], cut_df[to_plot[info_i][0]], c=to_plot[info_i][2])
    plt.ylabel(to_plot[info_i][1])
    for rown in range(notes_df.shape[0]):
        plt.axvline(x=notes_df.iloc[rown][0], color='black', ls='--', label=notes_df.iloc[rown][1])
        lev = (rown+1)/(notes_df.shape[0]+1)
        text_place = min(cut_df[to_plot[info_i][0]]) + lev * \
            (max(cut_df[to_plot[info_i][0]]) - min(cut_df[to_plot[info_i][0]]))
        plt.annotate(notes_df.iloc[rown][1], xy=(notes_df.iloc[rown][0], text_place))
plt.suptitle('r2: ' + str(round(r_value, 3))+'\nShift = ' + str(round(ishift/10, 3)))

plt.xlabel("Time")

# plt.legend()
plt.show(block=True)

print(file_number)
cut_df.to_csv('Cobbity9_run'+str(file_number)+'.csv', index=False)
