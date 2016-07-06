from beer_counter import SerialReader
from fotr_score import Score
import time
import sys, getopt

def run(person, borders):
    strPort = '/dev/ttyACM0'
    #strPort = args.port

    print('reading from serial port %s...' % strPort)
    if person not in ["sin","oce"]:
        assert("Invalid person")
    serial = SerialReader(strPort, borders)
    score = Score(person)
    start_time = time.time()
    while True:
        serial.read()
        if time.time()-start_time > 5:
            start_time = time.time()
            if not score.update():
                break;



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