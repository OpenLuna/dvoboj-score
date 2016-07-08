# -*- coding: utf-8 -*-

import sys, serial
import sys
import numpy as np
from time import sleep
from collections import deque
import re
import requests

class SerialReader:
    def __init__(self, strPort, borders):
        # open serial port
        print "Serial init start"
        self.ser = serial.Serial(strPort, 9600)
        self.counters = [BeerCounter(250) for i in range(borders)]
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
    def __init__(self, maxLen):
        # open serial port
        #self.ser = serial.Serial(strPort, 9600)

        self.ax = deque([0.0]*maxLen)

        self.maxLen = maxLen
        self.isIn = False
        self.framesIn = 0
        self.framesOut = 0
        self.counter = 0
    
    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        #assert(len(data) == 0)      
        self.addToBuf(self.ax, float(data)*10.0)
        #print "dodal", data
        minumum = min(self.ax)
        if abs(np.gradient(self.ax)[0])>0.1:
            print np.gradient(self.ax)[0]
        grad = np.gradient(self.ax)
        self.az=[85 if a>0.2 else 0 for i, a in enumerate(grad)]
        self.at=[a*20+20 for a in np.gradient(self.az)]

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
                print "send beer"
                requests.get("http://knedl.si/djnd/add/polica")
                print "Števec piru: " + str(self.counter)
        else:
            self.framesOut += 1
            if np.gradient(self.ax)[0]<-2 and self.framesOut > 50:
                self.isIn = True
                self.framesIn = 0
    """
    # update data
    def update(self):
        try:
            line = self.ser.readline()
            print line
            line = re.sub('\r\n', '', line)
            try:
                data = [float(val) for val in line.split(" ")]
            except:
                data = [0.0]
                #print data
            if(len(data) > 0):
                self.add(data)
        except KeyboardInterrupt:
            print('exiting')

        return
    """
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
    serial = SerialReader(strPort, 2)
    print('plotting data...')

    while True:

        #counter.update()
        serial.read()

    # clean up
    counter.close()

    print('exiting.')

# call main
if __name__ == '__main__':
    main()