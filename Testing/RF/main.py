import pandas as pd
import matplotlib.pyplot as plt

cut_df = pd.read_csv("RF_calibrate7.csv")

print(cut_df.head())

cut_df = cut_df  # .query("Shift > 7.15").query("Shift < 7.25")

plt.subplot(4, 1, 1)
plt.plot(cut_df['Freq'])
plt.ylabel("Resonant\nFrequency Hz")
plt.subplot(4, 1, 2)
plt.plot(cut_df['Amp'], c='g')
plt.ylabel("Amplitude")
plt.subplot(4, 1, 3)
plt.plot(cut_df['Shift'], c='purple')
plt.ylabel("Shift")
plt.subplot(4, 1, 4)
plt.plot(cut_df['temp'], c='yellow')
plt.ylabel("Temp")


plt.show()
