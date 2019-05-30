from ad9833 import AD9833
from pyb import Pin
from pyb import SPI
from specialmath import SpecialMath

import pyb
import array
import math
import utime
print("(Main program started)")


blueled = pyb.LED(4)
ss = Pin('Y5', Pin.OUT_PP)
spi = SPI(2, SPI.MASTER, baudrate=9600, polarity=1, phase=0, firstbit=SPI.MSB)


wave = AD9833(spi, ss)

blue_uart = pyb.UART(6, 9600)
blue_uart.init(9600, bits=8, stop=1, parity=None)

# pyb.repl_uart(blue_uart)

blue_uart.write("Warming up!")


# Initial variables
spw = 10        # Samples per wave
WAVES = 1000      # Number of waves to take an average from
freq = 17000    # Frequency in Hz


blue_uart.write("Started")

wave.set_freq(freq)
wave.set_type(0)
wave.send()

utime.sleep(2)

wave.set_freq(freq)
wave.set_type(0)
wave.send()


def send(wave, freq):
    wave.set_freq(freq)
    wave.send()


'''
mul = 10
for i in range(1500, 1900):
    wave.set_freq(+i*mul)
    wave.send()
    print(wave.freq)
    pyb.delay(50)

'''

adc1 = pyb.ADC(pyb.Pin.board.Y11)  # create an ADC on pin X1
adc2 = pyb.ADC(pyb.Pin.board.Y12)  # create an ADC on pin X2


tim = pyb.Timer(8, freq=200000)        # Create timer
buf1 = bytearray(WAVES*spw)  # create a buffer
buf2 = bytearray(WAVES*spw)  # create a buffe
# read analog values into buffers at 100Hz (takes one second)
pyb.ADC.read_timed_multi((adc1, adc2), (buf1, buf2), tim)


sm = SpecialMath()
(sm.hp_amp, sm.hp_sft) = (0, 0)


def record(f):
    tim = pyb.Timer(8, freq=f*spw)        # Create timer
    buf1 = bytearray(WAVES*spw)  # create a buffer
    buf2 = bytearray(WAVES*spw)  # create a buffe
    # read analog values into buffers at 100Hz (takes one second)
    pyb.ADC.read_timed_multi((adc1, adc2), (buf1, buf2), tim)

    listc = []

    for i in range(spw):
        listc.append(0)
    count = 0
    for n in range(len(buf1)):
        if count > spw-1:
            count = 0
        listc[count] += buf1[n]
        count += 1

    listd = []
    for i in range(spw):
        listd.append(0)
    count = 0
    for n in range(len(buf2)):
        if count > spw-1:
            count = 0
        listd[count] += buf2[n]
        count += 1
    # (a,s) = sm.fit_sin(listd,10)
    # print(listd)
    (a1, s1) = sm.fit_sin(listc, 3)
    # print("-")
    data_mean = sm.mean(listd)
    for d in range(0, len(listd)):
        listd[d] -= data_mean

    # total wave - Hp to get Hs
    sm.hp = sm.gen_sin(10, sm.hp_amp, s1 + sm.hp_sft)

    listout = [x - y for x, y in zip(listd, sm.hp)]
    (a2, s2) = sm.fit_sin(listout, 3)
    # print(listout)
    # print('Hp - Amp: %f  Sft: %f' % (a1,s1))
    # print('Hs - Amp: %f  Sft: %f' % (a2,s2))
    # print(s2-s1)

    if s2-s1 < 0:
        return(a1, a2, s2-s1 + spw)
    else:
        return(a1, a2, s2-s1)


'''
outfile = open('out.csv', 'w')

for freq in range(1600, 1800):
    wave.set_freq(freq*10)
    wave.send()
    (or_amp, amp, sft) = record(freq*10)
    print(freq*10, amp)
    blue_uart.write('%s, %s, %s' % (
        int(freq*10),
        int(amp),
        round(sft, 2)))
    outfile.write('%s,%s' % (freq*100, amp))
outfile.close()

'''

count = 0
rolling_amp = []
rolling_oramp = []
rolling_sft = []
callibrate = []
Hp_prev = 0
while True:
    print("------------------------------" + str(freq))
    (or_amp, amp, sft) = record(freq)
    print('%s, %s, %s' % (count, amp, sft))
    rolling_amp.append(amp)
    rolling_sft.append(sft)
    rolling_oramp.append(or_amp)
    if len(rolling_amp) > 4:
        blue_uart.write('%s, %s, %s' % (
            int(count),
            int(sum(rolling_amp)/500),
            round(sum(rolling_sft)/5, 2)))
        count += 1
        rolling_amp.pop(0)
        rolling_sft.pop(0)
        rolling_oramp.pop(0)
        blueled.toggle()
        lim = 20
        if count == lim and False:    # remove _ and False _ to get working again
            callibrate.append([amp, sft])
            # print(callibrate)
            [a, b] = [sum(x) for x in zip(*callibrate)]

            print("Hp:", a/lim, b/lim)
            if Hp_prev == round(float(a/lim), -2):
                blue_uart.write('Calibrated!!!!')
                (sm.hp_amp, sm.hp_sft) = (a/lim, b/lim)
            else:
                Hp_prev = round(float(a/lim), -2)
                blue_uart.write('Calibrating...')
                callibrate = []
                count = 0

        elif count < lim:
            callibrate.append([amp, sft])
