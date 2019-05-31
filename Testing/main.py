# This is for testing the Hbridge

from pyb import Pin, Timer

p1 = Pin('X1')  # X1 has TIM2, CH1
p2 = Pin('X3')  # X1 has TIM2, CH1
tim = Timer(2, freq=17100)

ch1 = tim.channel(1, Timer.PWM, pin=p1)
ch2 = tim.channel(3, Timer.PWM_INVERTED, pin=p2)
ch1.pulse_width_percent(50)
ch2.pulse_width_percent(50)
