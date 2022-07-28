from BluetoothServer import BluetoothServer
import json
import WifiConnect
import RPi.GPIO as GPIO
import requests
class HubBluetooth(BluetoothServer):
    def __init__(self):

        BluetoothServer.__init__(self)
        # self.riddle = ""

    def handleMessage(self, message):
        print("received: " + message)
        data = json.loads(message)
        WifiConnect.connect(data['ssid'], data['password'])
        # self.riddle = requests.get("https://qr-scavange.herokuapp.com/")
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(13, GPIO.LOW)
#         self.send('LOW' if int(message) < 50 else 'HIGH')
