import paho.mqtt.client as paho
import time
import random

# init broker
broker = "127.0.0.1"
port = 1883

client = paho.Client("mockup_data")
client.connect(broker, port)

i = 0
client.publish("main/sub0/sub0","Hello")
while(True):
    publish_string = ""
    if i % 2 == 0:
        publish_string = "true"
        i = i + 1
    else:
        publish_string = "false"
        i = i - 1

    for j in range (1,21):
        client.publish("main/room"+str(j)+"/light", publish_string)    
        client.publish("main/room"+str(j)+"/temp", random.randrange(18,24,1))

        for k in range(1,4):
            status_string = "OK"
            if j % k == 0:
                status_string = "WARNING"


            client.publish("main/room"+str(j)+"/devices/device"+str(k)+"/status", status_string) 
            client.publish("main/room"+str(j)+"/devices/device"+str(k)+"/power_on", publish_string) 


    time.sleep(1)
    print("loop")