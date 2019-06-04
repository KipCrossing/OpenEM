'''

import pyb
from pyb import Pin, Timer, LED


while True:
    tim2 = Timer(2, freq=17100)
    tim9 = Timer(9, freq=17100*10)
    adc1 = pyb.ADC(pyb.Pin.board.X3)
    buf = bytearray(20)

    ch1 = tim2.channel(1, Timer.PWM, pin=Pin.board.X1)
    ch2 = tim2.channel(2, Timer.PWM_INVERTED, pin=Pin.board.X2)
    adc1.read_timed(buf, tim9)
    print(list(buf))



from pyb import Pin, Timer
import pyb


p1 = Pin('X1')  # X1 has TIM2, CH1
p2 = Pin('X3')  # X1 has TIM2, CH1
tim = Timer(2, freq=8)

ch1 = tim.channel(1, Timer.PWM, pin=p1)
ch2 = tim.channel(3, Timer.PWM_INVERTED, pin=p2)
ch1.pulse_width_percent(50)
ch2.pulse_width_percent(50)

adc1 = pyb.ADC(pyb.Pin.board.Y11)  # create an ADC on pin X1
buf = bytearray(20)
adc1.read_timed(buf, tim)


#################################

adc1 = pyb.ADC(pyb.Pin.board.Y11)  # create an ADC on pin X1
adc2 = pyb.ADC(pyb.Pin.board.Y12)  # create an ADC on pin X2

tim = pyb.Timer(8, freq=17100*10)  # Create timer
buf1 = bytearray(WAVES*spw)  # create a buffer
buf2 = bytearray(WAVES*spw)  # create a buffe

# read analog values into buffers at 100Hz (takes one second)
pyb.ADC.read_timed_multi((adc1, adc2), (buf1, buf2), tim)

####################

adc1 = pyb.ADC(pyb.Pin.board.Y11)  # create an ADC on pin X1
adc2 = pyb.ADC(pyb.Pin.board.Y12)  # create an ADC on pin X2

tim = pyb.Timer(5, prescaler=4912, period=999)  # Create timer
buf1 = bytearray(WAVES*spw)  # create a buffer
buf2 = bytearray(WAVES*spw)  # create a buffe

# read analog values into buffers at 100Hz (takes one second)
pyb.ADC.read_timed_multi((adc1, adc2), (buf1, buf2), tim)

ch1 = tim.channel(1, Timer.PWM, pin=Pin.board.X7)
###################################3

# 171079
import pyb
tim = pyb.Timer(5, prescaler=245, period=9, div=4)

adc1 = pyb.ADC(pyb.Pin.board.X3)
buf = bytearray(100)
adc1.read_timed(buf, tim)
print(list(buf))


oc1 = tim.channel(1, pyb.Timer.OC_TOGGLE, pin=pyb.Pin.board.X1)
oc1.compare(0)

oc2 = tim.channel(2, pyb.Timer.OC_TOGGLE, pin=pyb.Pin.board.X2)
oc2.compare(0)

def next(i,oc):
    i += 1
    oc2.compare(i)
    return(i)

num = 0
tim.callback(lambda t: num = next(num,oc2))
'''
