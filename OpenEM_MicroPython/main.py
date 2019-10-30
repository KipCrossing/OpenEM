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
greenled = pyb.LED(1)

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
WAVES = 500      # Number of waves to take an average from
freq = 14000    # Frequency in Hz

# send wave
wave.set_freq(freq)
wave.set_type(0)
wave.send()

# check temp sensor
sht31_t, sht31_h = sht31sensor.get_temp_humi()

wait = True
while wait:
    print('Blue Out:')
    if b'BTM-U' == blue_uart.read():
        print("Start")
        wait = False
    pyb.delay(1000)


# pyb.repl_uart(blue_uart)

blue_uart.write("Warming up!\n")


blue_uart.write("Started")


utime.sleep(2)

wave.set_freq(freq)
wave.set_type(0)
wave.send()


# Timers for ADC's
adc1 = pyb.ADC(pyb.Pin.board.Y11)  # create an ADC on pin X11
adc2 = pyb.ADC(pyb.Pin.board.X4)  # create an ADC on pin X4

adc_voltage = pyb.ADC(pyb.Pin.board.Y12)

voltage = (adc_voltage.read()/4096)*14.12


adcall = pyb.ADCAll(12, 0x70000)  # 12 bit resolution, internal channels
coretemp = adcall.read_core_temp()

# tim = pyb.Timer(8, freq=200000)        # Create timer
# buf1 = bytearray(WAVES*spw)  # create a buffer
# buf2 = bytearray(WAVES*spw)  # create a buffe
# # read analog values into buffers at 100Hz (takes one second)
# pyb.ADC.read_timed_multi((adc1, adc2), (buf1, buf2), tim)


sm = SpecialMath()

(sm.hp_amp, sm.hp_sft) = (0, 0)

# Output File
outfile = open('out.csv', 'w')
outfile.write("i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,\n")
outfile.close()


def record(f, tim):
    # tim = pyb.Timer(8, freq=f*spw)        # Create timer
    # bytearray(WAVES*spw)  # create a buffer
    buf1 = array.array('H', (0 for i in range(WAVES*spw)))
    buf2 = array.array('H', (0 for i in range(WAVES*spw)))  # create a buffe
    # read analog values into buffers at 100Hz (takes one second)

    tcheck = pyb.ADC.read_timed_multi((adc1, adc2), (buf1, buf2), tim)
    # print(tcheck)

    listc = []

    for i in range(spw):
        listc.append(0)
    count = 0
    for n in range(len(buf1)):
        if count > spw-1:
            count = 0
        listc[count] += buf1[n]
        count += 1
    buf1 = None
    listd = []
    for i in range(spw):
        listd.append(0)
    count = 0
    for n in range(len(buf2)):
        if count > spw-1:
            count = 0
        listd[count] += buf2[n]
        count += 1
    # (a,s) = sm.fit_sin(listd,6)
    buf1 = None
    (a1, s1) = sm.fit_sin(listc, 6)
    # print("-")
    data_mean = sm.mean(listd)
    # print(data_mean)
    for d in range(0, len(listd)):
        listd[d] -= data_mean

    # total wave - Hp to get Hs
    if sm.hp_amp:
        sm.hp = sm.gen_sin(10, sm.hp_amp, s1 + sm.hp_sft)
        listout = [x - y for x, y in zip(listd, sm.hp)]
    else:
        listout = listd
    # print(listout)
    # outtext = ''
    # for d in listout:
    #     outtext += str(d)+','
    # outfile = open('out.csv', 'a')
    # outfile.write(outtext+"\n")
    # outfile.close()

    (a2, s2) = sm.fit_sin(listout, 6)
    # print(listout)
    # print('Hp - Amp: %f  Sft: %f' % (a1,s1))
    # print('Hs - Amp: %f  Sft: %f' % (a2,s2))
    # print(s2-s1)

    if s2-s1 < 0:
        return(a1, a2, s2-s1 + spw, data_mean)
    else:
        return(a1, a2, s2-s1, data_mean)


outfile = open('RF_calibrate.csv', 'w')
outfile.write("Freq,Amp,Shift,tim_freq,temp,meanW\n")
outfile.close()

while True:
    step_list = [1000, 100, 10, 1]
    mid = 9000
    max_amp = 0
    max_freq = 0
    max_sft = 0
    tim_freq = 1
    target_sft = 100
    RF_range_file = open("FR_range.csv", 'w')
    RF_range_file.write("Freq,Amp,Shift\n")
    for step in step_list:
        for i in range(-5, 6):
            f = mid + i*step
            if step != 1 and step != 2:
                tim = pyb.Timer(8, freq=f*spw)
                freq = int(tim.freq()/float(spw))
            else:
                freq = f
            wave.set_freq(freq)
            wave.send()
            pyb.delay(50)
            greenled.toggle()
            # blue_uart.write("Checking: {}\n".format(freq))
            ampl = []
            sftl = []
            ml = []
            for j in range(4):
                (or_amp, amp, sft, m) = record(freq, tim)
                ampl.append(amp)
                sftl.append(sft)
                ml.append(m)
            outline = "{},{},{}".format(freq, sm.mean(ampl), sm.mean(sftl))
            RF_range_file.write(outline + "\n")
            if sm.mean(ampl) > max_amp:
                max_amp = sm.mean(ampl)
                max_freq = wave.freq
                max_sft = round(sm.mean(sftl), 3)
                tim_freq = tim.freq()
                max_m = sm.mean(ml)
        mid = max_freq

    sht31_t, sht31_h = sht31sensor.get_temp_humi()
    outfile = open('RF_calibrate.csv', 'a')
    output = "{},{},{}".format(max_freq, int(max_amp), max_sft)
    outfile.write(output+",{},{},{}\n".format(tim_freq, sht31_t, max_m))
    blue_uart.write(output)
    print(output)
    blueled.toggle()
    greenled.toggle()
    outfile.close()
    RF_range_file.close()

'''
# Output File
outfile = open('OpenEM_data.csv', 'w')
outfile.write("ID,Amp,Shift,Shift_out,Voltage,Temp,Humidity,CoreTemp,Hs,Hp,Wmean\n")
outfile.close()


count = 0

callibrate = []
Hp_prev = 0
calivbate = True

c_amp = 0
c_sft = 0


freq = max_freq
wave.set_freq(freq)
wave.send()
pyb.delay(2000)
blue_uart.write('\nTimer freq: {}'.format(tim_freq))


tim = pyb.Timer(8, freq=tim_freq)
pyb.delay(2000)


ampl = []
sftl = []
for j in range(15):
    (or_amp, amp, sft, m) = record(freq, tim)
    ampl.append(amp)
    sftl.append(sft)
    blue_uart.write("Calibrate: {}%".format(j))
    print(amp, sft)
(sm.hp_amp, sm.hp_sft) = (sm.mean(ampl), sm.mean(sftl))

outfile = open('RF_calibrate.csv', 'a')
outfile.write("Hp,{},{}\n".format(sm.hp_amp, sm.hp_sft))

blue_uart.write("Calibrated! \nAmp: {} \nShift {}".format(sm.hp_amp, sm.hp_sft))


amp_roll = []
sft_roll = []


while True:
    print("------------------------------" + str(freq))
    blueled.toggle()
    ampl = []
    sftl = []
    for j in range(10):
        (or_amp, amp, sft, m) = record(freq, tim)
        print(amp)
        ampl.append(amp)
        sftl.append(sft)
    ampm = sm.mean(ampl)
    sftm = sm.mean(sftl)
    sht31_t, sht31_h = sht31sensor.get_temp_humi()
    coretemp = adcall.read_core_temp()
    voltage = (adc_voltage.read()/4096)*14.12 + 1

    if sft - sm.hp_sft < 0:
        sft_out = sft - sm.hp_sft + spw
    else:
        sft_out = sft - sm.hp_sft

    Hp = amp*math.sin(math.pi*2*sft_out/spw)
    Hs = -amp*math.cos(math.pi*2*sft_out/spw)

    amp_roll.append(ampm)
    sft_roll.append(sftm)
    if len(amp_roll) > 4:
        amp_roll.pop(0)
        sft_roll.pop(0)

    out_string = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (count,
                                                                   amp,
                                                                   sft,
                                                                   sft_out,
                                                                   voltage,
                                                                   sht31_t,
                                                                   sht31_h,
                                                                   coretemp,
                                                                   Hs,
                                                                   Hp,
                                                                   m)

    print(out_string)
    outfile = open('OpenEM_data.csv', 'a')
    outfile.write(out_string)
    outfile.close()

    blue_uart.write('%s, %s, %s' % (
        count,
        int(sm.mean(amp_roll)),
        sm.mean(sft_roll)))

    count += 1
'''
