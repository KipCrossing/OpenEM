# A discussion on analysing the data containing the primary and secondary waves

In this section, we will discuss approaches used to obtain our primary and secondary waves from our input data.

First, we obtain a list of data that is a representation of the primary wave that was obtained during calibration.

```python
Hp = [-6583,    580,    7477,    11508,    11147,    6558,    -540,    -7415,    -11523,    -11209]
```

We then approximate the Amplitude and phase shift using:

```python
import specialmath
sm = specialmath.SpecialMath()
(amp, sft) = sm.fit_sin(Hp, 5)
```

Note: the shift `sft` is relative to the transmitted wave and is observer by another ADC From these, we can generate a new the "perfect wave" using:

```python
Hp_fit = sm.gen_sin(10, amp, sft)
```

We can now get the values for the "perfect wave":

```python
>>> print(Hp_fit)
[-6570.65308724154, 550.1017952045793, 7460.736489154883, 11521.623425354583, 11181.64181864582, 6570.6530872415415,-550.1017952045727, -7460.736489154878, -11521.623425354584, -11181.641818645821]
```

And by taking the difference of the two lists, we get the noise:

```python
[-12.34691276, 29.8982048, 16.26351085, -13.62342535, -34.64181865, -12.65308724, 10.1017952, 45.73648915, -1.376574645, -27.35818135]
```

By viewing this data on a graph, it may be shown that the difference is relatively minor:

![Hp_chart](Hp_chart.png)

Now, the by subtracting the primary wave data from the input data, we should approximate to zero far away from material. When close to material, input signal

![formula](Sum_formula.png)
