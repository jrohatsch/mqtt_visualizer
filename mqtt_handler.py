import paho.mqtt.client as paho
import time
from error_handler import *

client_id = "mqtt_visualizer_"+ str(time.time())

class MqttHandler:
    client = paho.Client(client_id)
    port = 1883
    address = "127.0.0.1"
    topic = "#"
    
    storage = None

    def add_storage(self, storage_instance):
        self.storage = storage_instance

    def on_message_tree(self, client, userdata, message):
        # remove '' and leading b
        # b'True' -> True
        value = str(message.payload)[2:-1]

        self.storage.add(message.topic, value)

    def failed_connect(self):
        save_error("Could not connect to " + self.address + ":" + str(self.port))
        save_error("Please ensure a mqtt broker is running.")

    def init(self):
        try:
            self.client.connect(self.address, self.port)
        except ConnectionRefusedError:
            self.failed_connect()
            return False
            
        self.client.on_message = self.on_message_tree
        self.client.subscribe(self.topic)
        return True

    def destroy(self):
        self.client.unsubscribe(self.topic)
        self.client.disconnect()
