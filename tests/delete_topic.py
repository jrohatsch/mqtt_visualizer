import paho.mqtt.client as paho
import time
import random

# init broker
broker = "127.0.0.1"
port = 1883

client = paho.Client("mockup_data")
client.connect(broker, port)

i = 0
client.publish("main/hello","Hello")

client.publish("main/to_delete_base/to_delete/sub1","Hello")
client.publish("main/to_delete_base/to_delete/sub2","Hello")

time.sleep(5)

# should not cause to delete whole tree
#client.publish("main/to_delete","")

time.sleep(5)
client.publish("main/to_delete_base/to_delete/sub1","")
client.publish("main/to_delete_base/to_delete/sub2","")

