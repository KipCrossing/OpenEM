import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

cut_df = pd.read_csv("RF_calibrate11.csv")

print(cut_df.head())
roll = 2
# cut_df['meanW'] = cut_df['meanW'].rolling(roll, center=True, min_periods=1).mean().shift(-15)

# cut_df = cut_df.query("Shift > 7.15").query("Shift < 7.25")


def make_plot(df):
    plotn = 5
    plt.subplot(plotn, 1, 1)
    plt.plot(df['Freq'])
    plt.ylabel("Resonant\nFrequency Hz")
    plt.subplot(plotn, 1, 2)
    plt.plot(df['Amp'], c='g')
    plt.ylabel("Amplitude")
    plt.subplot(plotn, 1, 3)
    plt.plot(df['Shift'], c='purple')
    plt.ylabel("Shift")
    plt.subplot(plotn, 1, 4)
    plt.plot(df['temp'], c='yellow')
    plt.ylabel("Temp")
    plt.subplot(plotn, 1, 5)
    plt.plot(df['meanW'], c='red')
    plt.ylabel("MeanW")
    plt.show()


x = cut_df['meanW']
y = cut_df["Amp"]

slope, intercept, r_value, p_value, std_err = stats.linregress(
    x, y)

print(slope, intercept)


def make_plot2(df):
    plt.subplot(4, 1, 1)
    plt.scatter(df['meanW'], df["Amp"], s=0.5)
    plt.subplot(4, 1, 2)
    plt.scatter(df['temp'], df["Amp"], s=0.5)
    plt.subplot(4, 1, 3)
    plt.scatter(df['temp'], df["meanW"], s=0.5)
    plt.show()


def make_plot3(df):
    plt.subplot(3, 1, 1)
    plt.plot(df['Amp'])
    plt.subplot(3, 1, 2)
    plt.plot(-df['temp'])
    plt.subplot(3, 1, 3)
    plt.scatter(df['Amp'], -df['temp'], s=1)
    plt.show()


def make_plot4(df):
    plt.scatter(df['temp'], df["Freq"], s=0.5)
    flist = [13.8, 15.8, 17.3, 18.4, 21.2, 22.5, 24.2, 26, 28.1, 31, 32.5]
    for r in flist:
        plt.axvline(x=r, color='black', ls='--', label='Opperating Freq')
    plt.show()


make_plot(cut_df)

make_plot2(cut_df)
# make_plot4(cut_df)


freq_list = []
for i in cut_df['Freq']:
    if i not in freq_list:
        freq_list.append(i)
freq_list .sort(reverse=True)
print(freq_list)


for i in freq_list:
    temp_df = cut_df.query("Freq =="+str(i))
    print(temp_df["Shift"].max(), temp_df["Shift"].min())
    # make_plot3(temp_df)
