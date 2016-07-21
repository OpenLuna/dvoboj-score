# -*- coding: utf-8 -*-

import sys, serial
import sys
import numpy as np
from time import sleep, time
from collections import deque
import re
import requests
from  multiprocessing import Process

class SerialReader:
    def __init__(self, strPort, borders, person):
        # open serial port
        print "Serial init start"
        self.ser = serial.Serial(strPort, 9600)
        self.counters = [BeerCounter(250, person, "Polica_"+str(i)) for i in range(borders)]
        print "Serial init done"

    # update data
    def read(self):
        try:
            line = self.ser.readline()
            print line
            line = re.sub('\r\n', '', line)
            try:
                datas = [float(val) for val in line.split(" ")]
            except:
                datas = [0.0]
                #print data
            if(len(datas) >= len(self.counters)):
                for counter, data in zip(self.counters, datas):
                    counter.add(data)
        except KeyboardInterrupt:
            print('exiting')

        return


# plot class
class BeerCounter:
    # constr
    def __init__(self, maxLen, person, name="polica"):
        # open serial port

        self.ax = deque([0.0]*maxLen)
        self.maxLen = maxLen
        self.isIn = False
        self.framesIn = 0
        self.framesOut = 0
        self.counter = 0

        self.beers=0
        self.person = person
        self.name=name
    
    # add to buffer
    def addToBuf(self, buf, val):
        buf.pop()
        buf.appendleft(val)

    def sendBeers(self):
        resp = requests.get("http://knedl.si/djnd/add/polica_"+self.person).status_code
        if resp == 200:
            self.beers = 0
            print "sent success"
        else:
            self.beers += 1
            print "sent fail", self.beers
        return
    # add data
    def add(self, data):
        self.addToBuf(self.ax, float(data)*10.0)

        #checker
        if self.isIn:
            self.framesIn += 1
            if self.framesIn > 250:
                self.isIn = False
                self.framesOut = 45
                print "time out"
            if np.gradient(self.ax)[0] > 2:# and self.framesIn > 1:
                self.isIn = False
                self.framesOut = 45
                self.counter += 1
                print "BEER BEER BEER BEER "+ self.name
                t2 = Process(target = self.sendBeers)
                t2.start()
                print "Števec piru: " + str(self.counter)
        else:
            self.framesOut += 1
            if np.gradient(self.ax)[0]<-2 and self.framesOut > 50:
                self.isIn = True
                self.framesIn = 0

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()    

# main() function
def main():  
    strPort = '/dev/ttyACM0'
    #strPort = args.port

    print('reading from serial port %s...' % strPort)

    #counter = BeerCounter(strPort, 250)
    serial = SerialReader(strPort, 2, "test")
    print('plotting data...')

    while True:

        #counter.update()
        start_time = time()
        serial.read()
        print time()-start_time

    # clean up
    counter.close()

    print('exiting.')

# call main
if __name__ == '__main__':
    main()
