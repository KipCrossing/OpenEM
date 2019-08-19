import sht31
import machine
import pyb
import array
import math
import utime
from pyb import Pin, Timer
from ad9833 import AD9833
from pyb import Pin
from pyb import SPI
from specialmath import SpecialMath


print("(Main program started)")


blueled = pyb.LED(4)


# Wave gen
ss = Pin('Y5', Pin.OUT_PP)
spi = SPI(2, SPI.MASTER, baudrate=9600, polarity=1, phase=0, firstbit=SPI.MSB)
wave = AD9833(spi, ss)

# Bluetooth
blue_uart = pyb.UART(6, 9600)
blue_uart.init(9600, bits=8, stop=1, parity=None)

# Temp sensor
SCLpin = 'Y9'
SDApin = 'Y10'
i2c = machine.I2C(sda=machine.Pin(SDApin), scl=machine.Pin(SCLpin), freq=400000)
sht31sensor = sht31.SHT31(i2c)


# Initial variables
spw = 10        # Samples per wave
WAVES = 700      # Number of waves to take an average from
freq = 17000    # Frequency in Hz

# send wave
wave.set_freq(freq)
wave.set_type(0)
wave.send()


wait = True
while wait:
    print('Blue Out:')
    if b'BTM-U' == blue_uart.read():
        print("Start")
        wait = False
    pyb.delay(1000)


# pyb.repl_uart(blue_uart)

blue_uart.write("Warming up!")


blue_uart.write("Started")


utime.sleep(2)

wave.set_freq(freq)
wave.set_type(0)
wave.send()


'''
mul = 10
for i in range(1500, 1900):
    wave.set_freq(+i*mul)
    wave.send()
    print(wave.freq)
    pyb.delay(50)

'''

# Timers for ADC's
adc1 = pyb.ADC(pyb.Pin.board.Y11)  # create an ADC on pin X1
adc2 = pyb.ADC(pyb.Pin.board.X4)  # create an ADC on pin X2

adc_voltage = pyb.ADC(pyb.Pin.board.Y12)

voltage = (adc_voltage.read()/4096)*14.12

tim = pyb.Timer(8, freq=200000)        # Create timer
buf1 = bytearray(WAVES*spw)  # create a buffer
buf2 = bytearray(WAVES*spw)  # create a buffe
# read analog values into buffers at 100Hz (takes one second)
pyb.ADC.read_timed_multi((adc1, adc2), (buf1, buf2), tim)


sm = SpecialMath()
(sm.hp_amp, sm.hp_sft) = (0, 0)

# Output File
outfile = open('out.csv', 'w')
outfile.write("i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,\n")
outfile.close()


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

    (a1, s1) = sm.fit_sin(listc, 3)
    # print("-")
    data_mean = sm.mean(listd)
    for d in range(0, len(listd)):
        listd[d] -= data_mean

    # total wave - Hp to get Hs
    # sm.hp = sm.gen_sin(10, sm.hp_amp, s1 + sm.hp_sft)

    listout = listd  # [x - y for x, y in zip(listd, sm.hp)]
    # print(listout)
    outtext = ''
    for d in listout:
        outtext += str(d)+','
    outfile = open('out.csv', 'a')
    outfile.write(outtext+"\n")
    outfile.close()

    (a2, s2) = sm.fit_sin(listout, 3)
    # print(listout)
    # print('Hp - Amp: %f  Sft: %f' % (a1,s1))
    # print('Hs - Amp: %f  Sft: %f' % (a2,s2))
    # print(s2-s1)

    if s2-s1 < 0:
        return(a1, a2, s2-s1 + spw)
    else:
        return(a1, a2, s2-s1)


# Output File
outfile = open('Calibrate_data.csv', 'w')
outfile.write("ID, Amp, Shift, Shift_out, Voltage, Temp, Humidity, Hs, Hp \n")
outfile.close()


count = 0

callibrate = []
Hp_prev = 0
calivbate = True

c_amp = 0
c_sft = 0

while True:
    print("------------------------------" + str(freq))
    (or_amp, amp, sft) = record(freq)
    sht31_t, sht31_h = sht31sensor.get_temp_humi()

    voltage = (adc_voltage.read()/4096)*14.12
    sm.hp_sft = 5.0 + 1.4
    if sft - sm.hp_sft < 0:
        sft_out = sft - sm.hp_sft + spw
    else:
        sft_out = sft - sm.hp_sft

    Hs = amp*math.sin(math.pi*2*sft_out/spw)
    Hp = amp*math.cos(math.pi*2*sft_out/spw)

    out_string = "%s, %s, %s, %s, %s, %s, %s, %s, %s \n" % (count,
                                                            amp,
                                                            sft,
                                                            sft_out,
                                                            voltage,
                                                            sht31_t,
                                                            sht31_h,
                                                            Hs,
                                                            Hp)
    print(out_string)
    outfile = open('Calibrate_data.csv', 'a')
    outfile.write(out_string)
    outfile.close()

    blue_uart.write('%s, %s, %s' % (
        round(sft_out, 2),
        int(Hs),
        int(Hp)))

    count += 1
