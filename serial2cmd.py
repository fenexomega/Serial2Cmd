#!/usr/bin/env python3
import sys, glob, serial, argparse, json, threading, subprocess
from time import sleep

def eprint(*args,**kwargs):
    print(*args,file=sys.stderr, **kwargs)


def setArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--baud',help='Specify Baud rate. Default is 9600.',type=int,default=9600)
    parser.add_argument('-p','--port',help='Specify Serial Port. Default is the first one found.')
    parser.add_argument('config',nargs='?',help='Config file to read. Default to $HOME/.serialcmd/config.json.',default='.serialcmd/config.json')
    return parser.parse_args()

class MainObject:

    serial = None
    running = False

    def __init__(self,config,port,baud):
        self.config = config
        self.port = port
        self.baud = baud

    # found at
    # http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    def serial_ports(self):
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

    def mapConfigFile(self,file):
        with open(file, 'r') as myfile:
            data=myfile.read().replace('\n', '')
        decoded = json.loads(data)
        return decoded

    def openJsonConfig(self, jsonFile):
        self.configMap = self.mapConfigFile(jsonFile)

    def configSerial(self,port,baud):
        if self.serial == None:
            self.serial = serial.Serial(port,baud)
            if not self.serial.isOpen():
                self.serial.open()
        else:
            self.serial.port = port
            self.serial.baud = baud

    def isRunning(self):
        return self.running

    def exec_loop(self):
        self.running = True
        self.openJsonConfig(self.config)
        if self.serial == None or not self.serial.isOpen():
            self.configSerial(self.port,self.baud)
        lastCommand = None
        while True:
            while self.serial.inWaiting() == 0:
                #function to sleep
                if not self.running:
                    return
                sleep(0.1)
            line = self.serial.readline().decode('utf-8').replace('\r\n','')
            if line == "FFFFFFFF" and not lastCommand == None:
                line = lastCommand
            else:
                lastCommand = line
            try:
                ExecThread(self.configMap[line]).start()
            except KeyError as e:
                print("Key",e,"Not Implemented")

class ExecThread(threading.Thread):
    def __init__(self,command):
        super().__init__()
        self.command = command

    def run(self):
        print("[" + super().getName() +"] running \'" + self.command + "\'")
        subprocess.call(self.command,shell=True)
        print("[" + super().getName() +"] Exiting")

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

    exec_loop()


    # DO SHIT
