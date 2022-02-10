import paho.mqtt.client as paho
import time

# init broker
broker = "127.0.0.1"
port = 1883

client = paho.Client("mockup_data")
client.connect(broker, port)

i = 0
client.publish("main/sub0/sub0","Hello")
while(True):
    publish_string = ""
    publish_temp = 0
    if i % 2 == 0:
        publish_string = "true"
        publish_temp = 21+i
        i = i + 1
    else:
        publish_string = "false"
        publish_temp = 22+i
        i = i - 1

    for j in range (0,20):
        client.publish("main/room"+str(j)+"/light", publish_string)    
        client.publish("main/room"+str(j)+"/temp", publish_temp)

        for k in range(0,3):
            client.publish("main/room"+str(j)+"/devices/device"+str(k), publish_temp) 


    time.sleep(0.2)
    print("loop")