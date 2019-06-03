# Powering the Transmitter coil with a H-Bridge

This directory to keep notes on powering the Transmitter with a H-Bridge

The current set up is to keep put chokes on the 12v-in and GND-in lines of The H Bridge.

## Outcomes

- Stable input signal
- No voltage drift
- Small amount of drift (maybe noise)

![alt text](Hp_wave.png) _Input wave at calibration location_

![alt text](Ht_time_graph.png) _Graph showing the stability of the input signal_

There seems to be no drift in readings over a long amount of time. The standard deviation is about 2.9 for input reading average of 603.0\. _Note: these readings are directly proportional to the value from the ADC_

Notes on above image:

- Where the readings are at about 600, this is when the OpenEM is in the calibration area (no conductive material near it)
- At the beginning this is when the OpenEM is being moved from the work bench
- The 2nd and 3rd variations are at two different location (in more in phase and the other out)
- The last variation is when the oscilloscope is attached and the impedance of the input amplifier changes
