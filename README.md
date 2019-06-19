# OpenEM Project

This repository contains the Files and code related to the OpenEM project.

See [TODO.md](Info/TODO.md) for the current to do list.

Notes for the H-bridge variation of the setup may be found [here](Testing/README.md)

## Notes Summary

The following are a summary of notes in regards to the development of the OpenEM project; including the materials and methods used.

- Pyboard with micropython
- PWM H-Bridge
- Matching coils with RF of 17100 Hz
- Rx coil and op-amp grounded to 2.5 volts
- ADC on pyboard 0-3.3v for Rx signal
- ADC on pyboard to record wave from AD9833
- Record both waves onto buffers - x rotations and 10 samples per wave
- Get average of each n samples for all waves
- Use the curve fitting algorithm to get the amplitude and starting phase of the waves
- Calculate the phase shift of the received wave from the gen wave for reference
- Calibrate the primary wave while OpenEM is placed high above the ground
- Subtract Hp from the total input wave (Record Hp values)
- Lower OpenEM to the ground - new readings should be Hs (Amp and sft)
- Send readings to phone over Bluetooth
- Use Open Data Mapper to saves readings and GPS into a file and put coloured pin on the map
- Perform OpenEM survey on the field
- Perform Dualem survey on the field
- Smooth OpenEM data with a 7 point average
- Load data into QGIS
- Interpolate data (kriging) for the field area into rasta files (All dualem con and OpenEM con)
- Compare points of each Raster
- Make a model of Open vs 1mHCPcon & 2mHCPcon
- Discuss

Lessons learnt:

- ADC side Rx coil at the centre wire for more stable reading
- The RF of the Rx coil will change depending on what side the coil is grounded (inner or outer)
- Make coils RIGID
- put choke inductor at the H-bridge power input
- Don't use a pre-amplifier as it changes the impedance and hence resonant frequency of the receiver coil
- Use a simple non inverting amplifier grounded at 2.5 volts
- Secure all cables so that they don't move
- Place received a coil at distance from the circuitry to avoid feedback noise

## PyBoard with MicroPython

There are several requirements and pre-requisites for the OpenEM project that need to be considered when deciding on the correct microcontroller. These include: High resolution and high sample rate ADC Fast processing power for complex algorithms Common interfaces including; I2C, SPI and UART to drive external hardware and sensors Rapid prototyping Expandable storage for logging The microcontroller that was chosen, as it meets the above criteria, is the PyBoard (Bell 2017). The PyBoard is based on the STM32F405RG ARM micro-processor with an operating frequency of 168 MHz. The ADC's have a 12-bit resolution a sample rate of up to 200 kHz. All common interfaces are included plus several GPIO pins. Further, the PyBoard has a micro SD card slot for expandable storage. Lastly, the PyBoard is powered by MicroPython and is ideal for rapid prototyping.

MicroPython is a Re-write of Python 3 that is designed to run on microcontrollers (reference). Further, python is a commonly used, simple programming language and, as such, is good for showcasing the methods and algorithms used when handling and analysing the data. The MicroPython code for the OpenEm project may be found [here](https://github.com/KipCrossing/OpenEM).

## H-bridge with the L298N

One of the objectives with the transmitter coil it to maximise the current flowing through it. According to the law of Biot-Savart [(Pappas 1983)](https://link-springer-com.ezproxy1.library.usyd.edu.au/content/pdf/10.1007%2FBF02721552.pdf), the magnetic flux density is directly proportional to current I

![alt text](Images/bsav.png)

Therefore, we need a low impedence way to supply max current and that will maximise the voltage to get the maximum current in the coil.

```
V = I*Z
```

Where Z is the impedance of the coil at frequency f. The working for this may be found [here](https://github.com/KipCrossing/Coil_Physics/blob/master/coil.py).

There are 3 advantages using a H-bridge. The first is that it can supply a high current [up to 4 amps](https://www.st.com/resource/en/datasheet/l298.pdf) and the second is that it can handle high voltages (up to 46 V DC). The Third is that the it provides an easy way to switch the polarity of the input voltage of the transmitter coil. This means by using a 12 V power supply,

## OpenEM Frequency

The frequency needs to be chosen whilst considering the following requirements:

- The sample rate of the ADC on the PyBoard and enough samples per wave to get a precise enough estimate of the waves properties (apm and shift)
- The higher the frequency, the higher the Emf (Faraday's law)
- The larger the area of Rx the larger the Emf
- The higher the frequency, the lower the capacitive reactance
- The higher the frequency, the higher the inductive reactance
- The coil needs to have practical dimensions for the resonant frequency

The max sample rate of the pyboard using the `pyb.ADC.read_timed_multi()` method is approximately 200 kHz. The reason multiple ADC channels need to be recorded at once is so that the phase shift, in reference to the original wave (AD9833) can be observed. Further at least 10 samples per wave is deemed as acceptable to get an estimate of the wave properties. Therefore the frequency needs to be less than 20 kHz.

### Resonant Frequency

The resonant frequency of a coil is determined by:

![alt text](Images/SRF.png)

Where:

- XC = capacitive reactance
- XL = inductive reactance
- C = capacitance
- L = inductance

### Coil Details

Wound on a ferrite core, these are the details of the coil configuration:

- Wire gauge: 0.5 mm
- Coil length: 100 mm (200 turns)
- Number of layers: 20
- Total turns: 40,000
- Ferrite core diameter: 10 mm

Coil Properties:

- RF = 17,100 Hz
- L = 514.3 mH
- R = 12.6 Ohms
- C = 0.16 nF

The Resonant Frequency (**RF**) was obtained by sweeping a wave in an adjacent coil and observing where the amplitude peaked. The Coils Inductance (**L**) and Resistance (**R**) were measured using an [LCR40](https://www.peakelec.co.uk/acatalog/lcr40-atlas-lcr-meter.html). Lastly the capacitance (**C**) was back calculated using the following relation for the RF:

```
RF = 1/(2*math.pi_math.sqrt(Inductance*Capacitance)
```

From here, we may determine the Total Reactance (**Xt**) and the Impedance (**Z**) of the coils using the following equations (ref):

```
def Total_Reactance(self, freq):
  L = 2*np.pi_freq_self.coil_inductance
  C = 1/(2*np.pi_freq_self.coil_capacitance)
  return abs(C-L)

def Impedance(self, freq):
  return np.sqrt(self.coil_resistance**2 + self.Total_Reactance(freq)**2)
```

- Xt: 2913.00 Ohms
- Z = 2913.05 Ohms

Note that the Resistace (**R**) is significantly lower than the Total Reactance (**Xt**) and therefor Xt is the major contributing factor in the Impedance (**Z**). These equations may be found the the [Coil_Physics](https://github.com/KipCrossing/Coil_Physics) repo.

### Coil winding methods

In order to get the correct RF, a frequency sweep generator was set up and the frequency at which the the amplitude was the greatest is the RF. Depending on weather the frequency needs to be higher or lower, the following is done: To get it high - unwind loops. To get lower - wind more loops. Generally, more turns makes the Inductance increase which in turn, makes the makes the RF lower (see above formula for RF). Further, the length of the ferrite core is another factor contributing to the RF of a coil.

This is done with a similar set-up to what will be used in the OpenEM amplification signal. The materials and method are:

- get wave generator -
- Control AD9833 over SPI from the pyboard using this [DRIVER](https://github.com/KipCrossing/Micropython-AD9833)
- amplify the signal with a mini 10 Watt amplifier
- sweep through a range of frequencies to determine which frequency has yields the highest amplitude.

![alt text](Images/RF_square_finder.gif)

_Graphic of frequency sweep_

![alt text](Images/Amp_freq_graph.png)

_Graph of Amp vs frequency_

_Note:_ by analysing the above data. the resonant frequency occurs at 17004 Hz. Therefore, the settings for the PWM timer and the ADC timers are as follows:

```
adc_period = 493
spw = 10  # Samples per wavesimilar
pwm_period = (adc_period+1)*spw - 1

tim2 = pyb.Timer(2, prescaler=0, period=adc_period)  # for ADCs
tim5 = pyb.Timer(5, prescaler=0, period=pwm_period)  # for PWMs
```

_Note: For consistency, the transmitter coil and the receiver coil are identical so that the RF's are the same for both_

## Notes on the use of the H-bridge

The H-bridge method wont work as a square wave. This is because the eddy currents in the ground need to be a sin wave which is not achieved with a square wave.

Observations were made that the primary wave did reduce and shift when close or on the ground. Therefore, this method may be a measure of the permeability of the ground.

This method requires more research into why this occurs.

It would be easy to implement into the AD9833 verso-in (On master branch) as the AD9833 can produce a square wave,
