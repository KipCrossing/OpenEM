from pyb import Pin, Timer
from ad9833 import AD9833
from pyb import Pin
from pyb import SPI
from specialmath import SpecialMath

import pyb
import array
import math
import utime
print("(Main program started)")


adc_period = 490
pwm_period = (adc_period+1)*10 - 1

tim2 = pyb.Timer(2, prescaler=0, period=adc_period)  # for ADCs
tim5 = pyb.Timer(5, prescaler=0, period=pwm_period)  # for PWMs

freq = tim5.freq()
print(freq)
spw = 10        # Samples per wave
WAVES = 1000      # Number of waves to take an average from

# set opposing up PWM's
ch5_3 = tim5.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3)
ch5_4 = tim5.channel(4, pyb.Timer.PWM_INVERTED, pin=pyb.Pin.board.X4,
                     polarity=pyb.Timer.FALLING)
ch5_3.pulse_width_percent(50)  # 50% duty cycle
ch5_4.pulse_width_percent(50)  # 50% duty cycle

# set up ADCs
adc_Y11 = pyb.ADC(pyb.Pin.board.Y11)
adc_Y12 = pyb.ADC(pyb.Pin.board.Y12)


blueled = pyb.LED(4)

# Start Bluetooth
blue_uart = pyb.UART(6, 9600)
blue_uart.init(9600, bits=8, stop=1, parity=None)
blue_uart.write("Warming up!")


# Initial variables


sm = SpecialMath()
(sm.hp_amp, sm.hp_sft) = (0, 0)


def record(f):
    buf1 = bytearray(WAVES*spw)  # create a buffer
    buf2 = bytearray(WAVES*spw)  # create a buffe
    # read analog values into buffers at 100Hz (takes one second)
    tim2.counter(0)
    tim5.counter(0)
    pyb.ADC.read_timed_multi((adc_Y11, adc_Y12), (buf1, buf2), tim2)

    # listc = []
    # for i in range(spw):
    #     listc.append(0)
    # count = 0
    # for n in range(len(buf1)):
    #     if count > spw-1:
    #         count = 0
    #     listc[count] += buf1[n]
    #     count += 1

    listd = []
    for i in range(spw):
        listd.append(0)
    count = 0
    for n in range(len(buf2)):
        if count > spw-1:
            count = 0
        listd[count] += buf2[n]
        count += 1

    data_mean = sm.mean(listd)
    for d in range(0, len(listd)):
        listd[d] -= data_mean

    # total wave - Hp to get Hs
    # sm.hp = sm.gen_sin(10, sm.hp_amp, s1 + sm.hp_sft)
    # listout = [x - y for x, y in zip(listc, sm.hp)]
    listout = listd
    # print(listout)
    (a, s) = sm.fit_sin(listout, 4)
    return(a, s)


count = 0

Hp_prev = 0
while True:
    blueled.toggle()
    # print("------------------------------" + str(freq))

    (amp, sft) = record(freq)
    print('%s, %s, %s' % (count, amp, sft))
    blue_uart.write('%s, %s, %s' % (
        int(count),
        int(amp),
        round(sft, 2)))

    count += 1
