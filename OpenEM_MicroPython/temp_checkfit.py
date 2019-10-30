from specialmath import SpecialMath
sm = SpecialMath()

outfile = open("out.csv", "w")

for sft in range(1000):
    lst = sm.gen_sin(10, 100, sft/100.0)
    (a, s) = sm.fit_sin(lst, 6)
    print(sft/100.0, a, s)
    outfile.write("{},{},{}\n2".format(sft/100.0, a, s))

outfile.close()
