import pyb
import machine
import sht31

SCLpin = 'Y9'
SDApin = 'Y10'

i2c = machine.I2C(sda=machine.Pin(SDApin), scl=machine.Pin(SCLpin), freq=400000)
sht31sensor = sht31.SHT31(i2c)

while True:
    sht31_t, sht31_h = sht31sensor.get_temp_humi()
    print(sht31_t, sht31_h)
    pyb.delay(1000)
