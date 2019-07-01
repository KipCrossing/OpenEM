import specialmath

sm = specialmath.SpecialMath()

Hp = [-6583,	580,	7477,	11508,	11147,	6558,	-540,	-7415,	-11523,	-11209]

(amp, sft) = sm.fit_sin(Hp, 5)


Hp_fit = sm.gen_sin(10, amp, sft)
print(Hp_fit)
