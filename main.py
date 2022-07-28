import RPi.GPIO as GPIO 
from time import sleep

from datetime import datetime
import sys
import time
import threading
from HubBluetooth import HubBluetooth
import subprocess
from SerialWatch import SerialWatch
import requests
import json

hubBluetooth = HubBluetooth()
serialWatch = SerialWatch()
button_down_time = 0
print("--------------------test------------------------")
try:
    text = json.loads(requests.get("https://qrtag-tum.herokuapp.com/riddle").text)
    serialWatch.riddle = text['riddle']+'$'+text['qrcode']
    print(requests.get("https://qrtag-tum.herokuapp.com/riddle").text)
    print("----------------------------")
    print("received riddle: " + text)
except:
    print("not connected")
print(serialWatch.riddle)
def button_callback(channel):
    global read_image, button_down_time
    
    
    if GPIO.input(7):
        button_up_time = time.time()
        if button_up_time - button_down_time > 4:
            print('down for more than 4 secs')
            GPIO.output(13, 0)
            cmd = "sudo sh activate_pairing.sh"
            subprocess.run(cmd.split())
    else:
        button_down_time = time.time()
        read_image = True
    # camera.start_preview()
    # sleep(3)
    # ~ camera.capture('image.jpg')
    # camera.stop_preview()
    # ~ ret, frame = camera.read()
    # ~ im=decodeCam(frame)

    

def button_up_callback(channel):
    global button_down_time
    button_up_time = time.time()
    if button_up_time - button_down_time > 2:
        print('down for more than 2 secs')

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
GPIO.output(13, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)
GPIO.add_event_detect(7, GPIO.BOTH, callback=button_callback) 

start_time = time.time()

try:
    bluetoothThread = threading.Thread(target=hubBluetooth.start)
    bluetoothThread.start()
    # serialWatch.riddle = "tesssst"
    serialThread = threading.Thread(target=serialWatch.run)
    serialThread.start()
    while True:
        now = time.time()
        if(now - start_time > 10):
            start_time = time.time()
            # ~ try:
            # ~ print("test")
            resp = requests.get("https://qrtag-tum.herokuapp.com/riddle").text
            text = json.loads(resp)
            serialWatch.riddle = text['riddle']+'$'+text['qrcode']
            print("received from server: " + serialWatch.riddle)
                # ~ serialWatch.riddle = requests.get("https://qr-scavange.herokuapp.com/").text
                # ~ print("received riddle: " + serialWatch.riddle)
            # ~ except Error as e:
                # ~ print(str(e))
        # print("test")
        pass
except KeyboardInterrupt:
    GPIO.cleanup() # Clean up
    hubBluetooth.close()
    serialWatch.end()
    bluetoothThread.join()
    serialThread.join()
    sys.exit(0)

except:
    print("error")
