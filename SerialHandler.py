import sys
import serial
import glob
import re
class SerialHandler:

    """ Class for handling the initial serial connection between the hub and the
     device """
    def __init__(self):
        self.ports = []
        self.updatePorts()
        self._serial = None

    def updatePorts(self):
        self.ports = self._findSerialPorts()

    def begin(self, port, baudRate=115200, timeout=1):
        self._serial = serial.Serial(port=port, baudrate=baudRate, timeout=timeout, write_timeout=1)

    def end(self):
        self._serial.flush()
        self._serial.close()
        self._serial = None

    def write(self, msg):
        if not self._serial:
            print("serial object not associated")
            return
        self._serial.write(msg.encode())

    def readLine(self):
        if not self._serial:
            print("serial object not associated")
            return
        if not self._serial.inWaiting() <= 0:
            print("no serial")
            return
        return self._serial.read_until('\n')



    def _findSerialPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
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
