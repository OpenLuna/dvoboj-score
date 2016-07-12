from beer_counter import SerialReader
from fotr_score import Score
import time
import sys, getopt
import threading
from  multiprocessing import Process
from time import sleep

def run(person, borders):
    def beerLoop():
        while True:
            serial.read()
            #sleep(0.05)
            #print stop_threads
            if stop_threads:
                break

    strPort = '/dev/ttyACM0'
    #strPort = args.port

    print('reading from serial port %s...' % strPort)
    if person not in ["sin","oce"]:
        assert("Invalid person")

    serial = SerialReader(strPort, borders, person)
    score = Score(person)
    stop_threads = False
    t2 = Process(target = beerLoop)
    t2.start()
    
    while True:
        if not score.update():
            stop_threads=True
            t2.join()
	    stop_threads=True
            break
        sleep(5)



def main(argv):
    person = ''
    borders = ''
    try:
        opts, args = getopt.getopt(argv,"p:b:",["person=","sides="])
    except getopt.GetoptError:
        print 'dvoboj.py -p <person> -b <num_of_borders>', "error"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'dvoboj.py -p <person> -b <num_of_borders>'
            sys.exit()
        elif opt in ("-p", "--person"):
            person = arg
        elif opt in ("-b", "--borders"):
            borders = arg

    print 'Person is ', person
    print 'borders ', borders
    if person:
        if borders:
            run(person, int(borders))
        else:
            print "Run beer counter with 1 border"
            run(person, 1)
    else:
        print "Please insert a person"
        print 'dvoboj.py -p <person> -b <num_of_borders>'


if __name__ == "__main__":
   main(sys.argv[1:])
