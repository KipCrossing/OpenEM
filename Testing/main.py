# This is for testing the Hbridge

import pyb
import stm

# Using TIM2 and TIM5 because they correspond to AFs on X1 (TIM2 CH1) & X2 (TIM5 CH2)
# Choose prescaler/period values make sense for sample rate etc.
k = []

tim2 = pyb.Timer(2, prescaler=0, period=490)  # 20 kHz for ADC
# print(tim2.freq())

tim5 = pyb.Timer(5, prescaler=0, period=4909)  # 2 kHz for PWM

ch5_3 = tim5.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3)
ch5_4 = tim5.channel(4, pyb.Timer.PWM_INVERTED, pin=pyb.Pin.board.X4,
                     polarity=pyb.Timer.FALLING)
ch5_3.pulse_width_percent(50)  # 50% duty cycle
ch5_4.pulse_width_percent(50)  # 50% duty cycle

adc_X5 = pyb.ADC(pyb.Pin.board.X5)
adc_X6 = pyb.ADC(pyb.Pin.board.X6)

for i in range(1000):

    buf = bytearray(20000)
    pyb.delay(5)
    start = pyb.micros()
    tim2.counter(0)
    tim5.counter(0)
    adc_X5.read_timed(buf, tim2)
    end = pyb.micros()
    # print(end-start)
    listd = []
    for i in range(10):
        listd.append(0)
    count = 0
    for n in range(len(buf)):
        if count > 10-1:
            count = 0
        listd[count] += buf[n]
        count += 1
    if end - start == 116970:
        print(listd)
    pyb.delay(100)
#     print(str(listb[0]) + "," + str(listb[1]) + "," +
#           str(listb[2]) + "," + str(listb[3]) + "," + str(listb[4]))
#     if (listb[0] + listb[1] + listb[2] + listb[3] + listb[4]) > 1200:
#         print('Yes')
#         k.append(1)
#     else:
#         print('no')
#         k.append(0)
# print(k)
