# OpenEM Project

This reposotry contains the Files and code related to the OpenEM project.

# Notes

The following are a summary of notes in regards to the development of the OpenEM project; including the materials and methods used.

- Pyboard with micropython
- AD9833 wave generator
- 10 W amplifier
- Matching coils with RF of 17100 Hz
- Rx coil and op-amp grounded to 2.5 volts
- ADC on pyboard 0-3.3v for Rx signal
- ADC on pyboard to record wave from ad9833
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

Lessons learnt

- Ground Rx coil at the centre wire for more stable reading
- Make coils RIGID
- put choke inductors at the 10 W amplifier to reduce noise from the amplifier
- Don't use a preamplifier as it changes the resonant frequency of the receiver coil
- Use a simple non inverting amplifier grounded at 2.5 volts
- Secure all cables so that they don't move
- Place received a coil at distance from the circuitry to avoid feedback noise

## PyBoard with MicroPython

There are several requirements and pre-requisites for the OpenEM project that need to be considered when deciding on the correct microcontroller. These include: High resolution and high sample rate ADC Fast processing power for complex algorithms Common interfaces including; I2C, SBI and UART to drive external hardware and sensors Rapid prototyping Expandable storage for logging The microcontroller that was chosen, as it meets the above criteria, is the PyBoard (Bell 2017). The PyBoard is based on the STM32F405RG ARM micro-processor with an operating frequency of 168 MHz. The ADC's have a 12-bit resolution a sample rate of up to 200 KHz. All common interfaces are included plus several GPIO pins. Further, the PyBoard has a micro SD card slot for expandable storage. Lastly, the PyBoard is powered by MicroPython and is ideal for rapid prototyping.

MicroPython is a Re-write of Python 3 that is designed to run on microcontrollers (reference). Further, python is a commonly used, simple programming language and, as such, is good for showcasing the methods and algorithms used when handling and analysing the data. The MicroPython code for the OpenEm project may be found [here](https://github.com/KipCrossing/OpenEM).

## AD9833 Wave Gen

The first step, after establishing what microcontroller to use, is to generate a sine wave that can be adjusted to match the resonant frequency of the transmitter and receiver coils. Therefore, it is important to select a wave generator with a variable frequency that can be adjusted via a common interface. For this, the AD9833 was selected as is has a frequency range of 0.1 Hz to 12.5 MHz (Qi et al. 2015) and can be controlled over SBI. To set the frequency and wave type (sine, square or triangle) a a micropython library was made and can be found [here](https://github.com/KipCrossing/Micropython-AD9833). This signal is then amplified to the Transmitter coil.

## Amplifying the signal

One of the objectives with the transmitter coil it to maximise the current flowing through it. According to the law of Biot-Savart, the magnetic flux density is directly proportional to to current I

![alt text](Images/bsav.png)

Therefore, we need an amplifier to supply the current and that will maximise the voltage to get the maximum current.

```
V = I*Z
```

Where Z is the impedance of the coil at frequency f.

![alt text](Images/OpenEM_field_surveys.jpg)

![alt text](Images/OpenEM_calibration.jpg)

![alt text](https://github.com/KipCrossing/EMI_Field/blob/master/Cobbity8/Screenshots/OpenEM_con_Ave7_chipped.png)
