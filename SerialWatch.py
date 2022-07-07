from SerialHandler import SerialHandler
import time
import socket
import json
import sys
def onMQTTConnect(client, userdata, flags, rc):
    print("Connected to MQTT broker, result code: " + str(rc))
def onMQTTDisconnect():
    print("DISCONNECTED FROM MQTT BROKER")

def onMQTTMessage(client, userdata, msg):
    print("I received a message: " + str(msg.payload))

def getLocalIP():

    return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
                       [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])


class SerialWatch:
    def __init__(self):
        self.serialHandler = SerialHandler()
        self.baudRate = 115200
        self.configuredPorts = []
        self.riddle = ""
        self.stop = False

    def run(self):
        self.stop = False
        while not self.stop:
            self.serialHandler.updatePorts()
            if len(self.serialHandler.ports ) > 0:
                for port in self.serialHandler.ports:
                    if port not in self.configuredPorts:
                        self.configuredPorts.append(port)
                        print("inserted: " + port)

                        if self.riddle:
                            self.serialHandler.begin(port, self.baudRate)
                            send = self.riddle
                            print("sending: " + send)
                            try:
                                time.sleep(2)
                                self.serialHandler.write(send)
                            except:
                                print("write timeout")
                            # print("test")
                        
                        # while(True):
                        #     try:
                        #         str = self.serialHandler.readLine()
                        #         print "parsing: " + str
                        #         json.loads(str)
                        #     except KeyboardInterrupt:
                        #         sys.exit()
                        #     except:
                        #         print "could not parse"
                        #         continue
                        #
                        #     print "parsed: " + str
                        #     break
                        # str = ""
                        # while(str == ""):
                        #     str = self.serialHandler.readLine()

                        # print("received: " + str)
                        # id = str
                        # str = ""
                        # f = open("../homeAuto.conf", 'r')
                        # config = json.loads(f.read())

                        # send = json.dumps({"msg":"info", "data":[config["ssid"], config["wifiPass"], getLocalIP()]})
                        # print("sending: " + send)
                        # self.serialHandler.write(send)
                        # str = ""
                        # while (str == ""):
                            # str = self.serialHandler.readLine()
                        # print("received: " + str)
                        # send = "{\"msg\": \"ok\"}"
                        # print("sending: " + send)
                        # self.serialHandler.write(send)


            for configuredPort in self.configuredPorts:
                if configuredPort not in self.serialHandler.ports:
                    self.configuredPorts.remove(configuredPort)
                    print("removed: " + configuredPort)

            time.sleep(1)

    def end(self):
        self.stop = True
        self.serialHandler.end()


if __name__ == '__main__':
    s = SerialWatch()
    s.run()

