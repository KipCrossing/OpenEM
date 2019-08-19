filename_in = 'zones_X3.txt'
filename_out = 'zones_X3.csv'
f_in = open(filename_in, 'r')
f_out = open(filename_out, 'w')


for line in f_in:
    lineout = line.replace('\t', ',').replace(' ', ',')
    f_out.write(lineout)
f_in.close()
f_out.close()
