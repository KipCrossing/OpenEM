import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("FR_range.csv")

df['Freq2'] = df['Freq'] + 100

print(df.head())

df['Amp'] = df['Amp'].rolling(10, center=True, min_periods=1).mean()

print(df['Freq'][df['Amp'].idxmax()])

plt.subplot(2, 1, 1)
plt.plot(df['Freq2'], df['Amp'], c='b')
plt.plot(df['Freq'], df['Amp'], c='g')
plt.axvline(x=df['Freq'][df['Amp'].idxmax()], color='black', ls='--', label='Opperating Freq')
plt.annotate('Opperating Freq', xy=(df['Freq'][df['Amp'].idxmax()], 10000))
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(df['Freq2'], df['Shift'], c='red')
plt.plot(df['Freq'], df['Shift'], c='purple')
plt.axvline(x=df['Freq'][df['Amp'].idxmax()], color='black', ls='--', label='Opperating Freq')
plt.annotate('Opperating Freq', xy=(df['Freq'][df['Amp'].idxmax()], 5.5))
plt.ylabel("Shift (y/10)")
plt.xlabel("Freq (Hz)")
plt.show()
