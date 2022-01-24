import paho.mqtt.client as paho

broker = "127.0.0.1"
port = 1883

class MqttHandler:
    client = paho.Client("mqtt_visualizer")
    storage = None

    def add_storage(self, storage_instance):
        self.storage = storage_instance

    def on_message_tree(self, client, userdata, message):
        value = str(message.payload)[1:]

        self.storage.add(message.topic, value)

    def init(self):
        self.client.connect(broker, port)
        self.client.on_message = self.on_message_tree

    def start(self):
        self.client.subscribe("#")
        self.client.loop_start()

    def stop(self):
        self.client.unsubscribe("#")
        self.client.loop_stop()
