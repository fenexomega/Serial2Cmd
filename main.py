#!/usr/bin/env python3
import sys
import glob
import serial
import argparse
import json
import os
import subprocess
from time import sleep

def eprint(*args,**kwargs):
    print(*args,file=sys.stderr, **kwargs)


def setArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--baud',help='Specify Baud rate. Default is 9600.',type=int,default=9600)
    parser.add_argument('-p','--port',help='Specify Serial Port. Default is the first one found.')
    parser.add_argument('config',nargs='?',help='Config file to read. Default to $HOME/.serialcmd/config.json.',default='.serialcmd/config.json')
    return parser.parse_args()


# found at
# http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def mapConfigFile(file):
    with open(file, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    decoded = json.loads(data)
    return decoded

def configSerial(port,baud):
    return serial.Serial(port,baud)



if __name__ == "__main__":
    args = setArgs()
    ports = serial_ports()
    print("available ports:")
    for port in ports:
        print(port)
    if args.port == None:
            if len(ports) == 0:
                eprint("error: didn't found any ports. Exiting.")
                sys.exit(1)
            args.port = ports[0]
    jsonFile = mapConfigFile(args.config)

    ser = configSerial(args.port,args.baud)
    lastCommand = None
    while True:
        if not ser.isOpen():
            ser.open()
        while ser.inWaiting() == 0:
            #dormir por 100ms
            sleep(0.1)
        line = ser.readline().decode('utf-8').replace('\r\n','')

        if line == "FFFFFFFF" and not lastCommand == None:
            line = lastCommand
        else:
            lastCommand = line
        ser.close()
        pid = os.fork()
        if pid == 0:
            subprocess.call(jsonFile[line],shell=True)
            os._exit(0)
        else:
            continue



    # DO SHIT
