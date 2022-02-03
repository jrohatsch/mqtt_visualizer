import paho.mqtt.client as paho
import time

# init broker
broker = "127.0.0.1"
port = 1883

client = paho.Client("mockup_data")
client.connect(broker, port)

i = 0
while(True):
    publish_string = ""
    if i % 2 == 0:
        publish_string = "true"
        i = i + 1
    else:
        publish_string = "false"
        i = i - 1

    for j in range (0,10):
        for k in range (0,10):
            client.publish("main/sub"+str(j)+"/sub"+str(k), publish_string)    

    client.publish("main/sub0/sub0","Hello")

    time.sleep(1)
    print("loop")