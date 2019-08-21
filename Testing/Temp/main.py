import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('temp_data.csv', sep=',')


df['Amp rolling'] = df[' Amp'].rolling(50).mean()


print(df.head(10))

cut_df = df.query('ID > 2400').query('ID < 8200')


# plt.plot(cut_df['ID'], cut_df[' Temp']*1700)
# plt.plot(cut_df['ID'], cut_df['Amp rolling'])

plt.scatter(cut_df[' Temp'], cut_df['Amp rolling'], s=0.5)

plt.show()
