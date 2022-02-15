lorem_ipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
long_topic = "this_is_a_very_long_topic_name_with_numbers_1_2_3"

import paho.mqtt.client as paho

# init broker
broker = "127.0.0.1"
port = 1883

client = paho.Client("mockup_data")
client.connect(broker, port)

client.publish("main/sub", lorem_ipsum)

for i in range(10):
    client.publish("main/" + str(i) + "/" + long_topic , lorem_ipsum)