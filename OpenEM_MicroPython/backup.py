print("(Main program started) - WAVES = 32")

import pyb
import AD9833
import array


blue_uart = pyb.UART(2, 9600)
blue_uart.init(9600, bits=8, stop=1, parity=None)

# pyb.repl_uart(blue_uart)

blue_uart.write("Warming up!")



#Initial variables
spw = 64        # Samples per wave
WAVES = 32       # Number of waves to take an average from
freq = 10000    # Frequency in Hz

pyb.delay(1100)
AD9833.run(freq)
blue_uart.write("Warming up!")
pyb.delay(2000)
AD9833.run(freq)
blue_uart.write("Calibrating in 3")
pyb.delay(1000)
blue_uart.write("Calibrating in 2")
pyb.delay(1000)
blue_uart.write("Calibrating in 1")
pyb.delay(1000)

adc1 = pyb.ADC(pyb.Pin.board.X1)  # create an ADC on pin X1
adc2 = pyb.ADC(pyb.Pin.board.X2)  # create an ADC on pin X1



# This function takes a list abd makes a new list where each point is
# the average of the corrisponding point on the origional list and 
# 3 points either side; making an average from 7 points.
def sevenpointaverage(list2):
    #7 average
    filtered_list2 = list2

    tnum = 0
    for vd in list2:
        if tnum == 0:
            filtered_list2[tnum] = (list2[0]+list2[1]+list2[2]+list2[3]+list2[spw-3]+list2[spw-2]+list2[spw-1])/7.0
        elif tnum == 1:
            filtered_list2[tnum] = (list2[0]+list2[1]+list2[2]+list2[3]+list2[4]+list2[spw-2]+list2[spw-1])/7.0
        elif tnum == 2:
            filtered_list2[tnum] = (list2[0]+list2[1]+list2[2]+list2[3]+list2[4]+list2[5]+list2[spw-1])/7.0
        elif tnum == spw-1:
            filtered_list2[tnum] = (list2[0]+list2[1]+list2[2]+list2[spw-4]+list2[spw-3]+list2[spw-2]+list2[spw-1])/7.0
        elif tnum == spw-2:
            filtered_list2[tnum] = (list2[0]+list2[1]+list2[spw-5]+list2[spw-4]+list2[spw-3]+list2[spw-2]+list2[spw-1])/7.0
        elif tnum == spw-3:
            filtered_list2[tnum] = (list2[0]+list2[spw-6]+list2[spw-5]+list2[spw-4]+list2[spw-3]+list2[spw-2]+list2[spw-1])/7.0
        else:
            filtered_list2[tnum] = (list2[tnum-3]+list2[tnum-2]+list2[tnum-1]+list2[tnum]+list2[tnum+1]+list2[tnum+2]+list2[tnum+3])/7.0
    return(filtered_list2)




def phase(buf1,buf2):
    
    list1 = []
    list2 = []

    for moii in range(spw):
        list1.append(0)
        list2.append(0)
    
    i = 0
    #average over number of samples
    for value in buf1:

        if i > spw-1:
            i = 0
        list1[i] += value
        i += 1


    i = 0

    for value in buf2:

        if i > spw-1:
            i = 0
        list2[i] += value
        i += 1
    filtered_list1 = sevenpointaverage(list1)
    filtered_list2 = sevenpointaverage(list2)
    
    average1 = sum(filtered_list1)/float(len(filtered_list1))
    average2 = sum(filtered_list2)/float(len(filtered_list2))
    
    trigger1 = []

    trigger2 = []

    
    #Find point at which the trigger occurs
    a = 0
    for item in filtered_list1:
        if a < spw-1:
            if filtered_list1[a] < average1 and filtered_list1[a+1] > average1:
                trigger1.append(a)
        a += 1
    
    a = 0
    for item in filtered_list2:
        if a < spw-1:
            if filtered_list2[a] < average2 and filtered_list2[a+1] > average2:
                trigger2.append(a)
        a += 1
        
        

    faise = -1
    
    if len(trigger1) == 1 and len(trigger2) == 1:
        if trigger1[0] < trigger2[0]:
            faise = trigger2[0] - trigger1[0]

        if trigger1[0] > trigger2[0]:
            faise = trigger2[0] - trigger1[0] + spw
    else:
        trigger1.append(-1)
        
    return(int(faise),trigger1[0])

    



def inQUAD(buf2,trigger_phase):
        
    
    list2 = []
    outlist = []

    for moii in range(spw):
        list2.append(0)
        outlist.append(0)
    

    i = 0

    for value in buf2:

        if i > spw-1:
            i = 0
        list2[i] += value
        i += 1
    
    
    #7 average
    filtered_list2 = sevenpointaverage(list2)


        
        
        
    average2 = sum(filtered_list2)/float(len(filtered_list2))
    
    c = trigger_phase
    
    for i in range(64):
        if c>63:
            c=0
        outlist[i] = filtered_list2[c] - average2
        
        c+=1
    
    
    return(outlist)


# Generate the output file
import os
f = filenumber = 0
while not bool(f):
    filenumber += 1
    if not ('results'+str(filenumber)+'.csv' in os.listdir('Log')):
        f = open('/sd/Log/results'+str(filenumber)+'.csv', 'w')
        print('/sd/Log/results'+str(filenumber)+'.csv - created')



heading = []
for i in range(64):
    heading.append('S'+str(i+1))

f.write('ID,lat,lon,time,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % tuple(heading))

f.close()

heading = None

count = 0
ID = 0
thesum = []


modelist = []
themode = False
for i in range(64):
    thesum.append(0)
kip = 0


sampleave = 5.0

rollingaveragelist = []

running = True
GPS = ",,"
while running:
    kip+=1
    
    
    if blue_uart.any():
        line = blue_uart.readline()
        line = str(line,'utf-8')
        if line[-5:-1] == "BTM-":
            if line[-5:] == "BTM-F":
                print("Finish...")
                running = False
            if line[-5:] == "BTM-G":
                print("BTM-G")
                print(line[1:-5])
                char_check = False
                backup_str = ""
                for char in line[1:-5]:
                    if char == "G":
                        char_check = True
                    if char_check == True:
                        backup_str += char
                if char_check:
                    print(backup_str[2:])
                    GPS = backup_str[2:]
                else:
                    print(line[1:-5])
                    GPS = line[1:-5]
    
    buf1 = bytearray(WAVES*spw)  # create a buffer of 1000 bytes
    buf2 = bytearray(WAVES*spw)  # create a buffer of 1000 bytes
    postbuf = bytearray(WAVES*spw)
    smaplerate = spw*freq
    pyb.udelay(30)
    adc1.read_timed(buf1,smaplerate)
    adc2.read_timed(buf2, smaplerate)
    adc1.read_timed(postbuf,smaplerate)
    
    
    
    #(wphase, trigger_phase) = phase(buf1, buf2)
    (check, trigger_phase) = phase(buf1, postbuf)
    #blue_uart.write('%s,%s\n' % (check,trigger_phase))
    
    if kip < 50:
        modelist.append(check)
        #print(check)
    elif kip == 50:
        themode = max(set(modelist), key=modelist.count)
    
    
    if themode:
        if check == themode:

            inQUADlist = inQUAD(buf2, trigger_phase)
            for i in range(64):
                thesum[i] += round(inQUADlist[i]/(sampleave*10),2)
            count +=1


    if count == sampleave:
        output = str(ID)+',' + GPS + ',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % tuple(thesum)

        f = open('/sd/Log/results'+str(filenumber)+'.csv', 'a')
        f.write(output)
	f.close()
        print('%s,%s\n' % (ID,thesum[40]))
        blue_uart.write('%s,%s' % (ID,thesum[40]))

        
        for i in range(64):
            thesum[i] = 0
        count=0
        ID+=1
        GPS = ",,"
    



blue_uart.write("Finished!")                
f.close()


