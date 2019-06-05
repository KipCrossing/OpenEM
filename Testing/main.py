# This is for testing the Hbridge

import pyb
import stm

# Using TIM2 and TIM5 because they correspond to AFs on X1 (TIM2 CH1) & X2 (TIM5 CH2)
# Choose prescaler/period values make sense for sample rate etc.
k = []
for i in range(1000):
    tim2 = pyb.Timer(2, prescaler=0, period=490)  # 20 kHz for ADC
    ch2_1 = tim2.channel(1, pyb.Timer.IC, pin=pyb.Pin.board.X1, polarity=pyb.Timer.FALLING)
    # print(tim2.freq())
    PER = 4909
    tim5 = pyb.Timer(5, prescaler=0, period=PER)  # 2 kHz for PWM
    ch5_2 = tim5.channel(2, pyb.Timer.IC, pin=pyb.Pin.board.X2, polarity=pyb.Timer.FALLING)
    # print(tim5.freq())
    # Additional config to make TIM2 gated on TI1 (i.e. channel 1)
    smcr = stm.mem16[stm.TIM2 + stm.TIM_SMCR]
    smcr &= 0b1111111110001000
    smcr |= 0b0000000001010101   # TS = 101 (TI1), SMS = 101 (Gated)
    stm.mem16[stm.TIM2 + stm.TIM_SMCR] = smcr

    # Additional config to make TIM5 gated on TI2 (i.e. channel 2)
    smcr = stm.mem16[stm.TIM5 + stm.TIM_SMCR]
    smcr &= 0b1111111110001000
    smcr |= 0b0000000001100101   # TS = 110 (TI2), SMS = 101 (Gated)
    stm.mem16[stm.TIM5 + stm.TIM_SMCR] = smcr

    ch5_3 = tim5.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3, polarity=pyb.Timer.FALLING)
    ch5_3.pulse_width_percent(50)  # 50% duty cycle
    tim2.counter(490)
    tim5.counter(PER)

    tim14 = pyb.Timer(14, freq=2)
    # print(tim14.period())
    tim14.counter(0)
    ch14_8 = tim14.channel(1, pyb.Timer.OC_FORCED_ACTIVE, pin=pyb.Pin.board.X8)
    ch14_8 = tim14.channel(1, pyb.Timer.OC_INACTIVE, pin=pyb.Pin.board.X8)
    ch14_8.compare(tim14.period())
    print(tim14.counter())
    print(ch14_8.compare())

    adc = pyb.ADC(pyb.Pin.board.X4)
    buf = bytearray(201)
    tim14.counter(1)
    adc.read_timed(buf, tim2)  # Blocks on the USER button
    ch14_8 = tim14.channel(1, pyb.Timer.OC_FORCED_ACTIVE, pin=pyb.Pin.board.X8)
    tim2.deinit()
    tim5.deinit()
    tim14.deinit()
    listb = list(buf)
    listb.pop(0)
    print(str(listb[0]) + str(listb[1]) + str(listb[2]) + str(listb[3]) + str(listb[4]))
    if (listb[0] + listb[1] + listb[2] + listb[3] + listb[4]) > 1200:
        print('Yes')
        k.append(1)
    else:
        print('no')
        k.append(0)

print(k)
