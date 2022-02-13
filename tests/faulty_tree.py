import paho.mqtt.client as paho
import time

# init broker
broker = "127.0.0.1"
port = 1883

client = paho.Client("mockup_data")
client.connect(broker, port)

while(True):
    for i in range(3):
        client.publish("main/tree/key"+str(i), "value"+str(i))

    time.sleep(2)
    client.publish("main/tree", "faulty value")
    time.sleep(2)
    print("loop")

