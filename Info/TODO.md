# TO DO LIST

- [x] Wind coil for 17100 Hz
- [x] Use RF circuit to check RF
- [x] Check both amplifiers (easy connect)
- [x] Do H-Bride tests

  - Put on same circuit as Rx
  - Compare with choke

- [x] match ADC with PWM; see [timers](http://docs.micropython.org/en/latest/library/pyb.Timer.html)

  - Option 1: Make function and put on seperate timers
  - Option 2: Sync timers, see [this post](https://forum.micropython.org/viewtopic.php?t=986)
  - [x] I've made a post [here](https://forum.micropython.org/viewtopic.php?f=2&t=6513)

- [ ] Dual ADC and PWM

- [ ] Check different sweeps

- [ ] Output max and min ADC readings

- [ ] Set up H-Bridge circuit

  - test for noise
  - Non-inverting amp
  - blue-tooth (spare or pins for plug and play)
  - measure pulse with ADC read_multi()
  - Measure voltage circuit
  - Add temp sensor

- [ ] Measure voltage [circuit](https://startingelectronics.org/articles/arduino/measuring-voltage-with-arduino/)

- [ ] Show Hp vs freq graph (For 17100 Hz coil)

- [ ] Get data for `Ht - Hp = Hs` curves

- [ ] Add temperature sensor: [BME280](https://github.com/catdog2/mpy_bme280_esp8266)

- [ ] Do Hp vs temp

- [ ] Do voltage vs Hp test & find relationship

- [ ] Find temp relationship

- [ ] Do Hs vs temp

- [ ] Large Cobbity test

- [ ] Larger field test with ECe (Cores)
