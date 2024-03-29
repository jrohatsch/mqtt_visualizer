import paho.mqtt.client as paho
import time
from src.error_handler import *
import threading

client_id = "mqtt_visualizer_"+ str(time.time())

class MqttHandler:
    client = paho.Client(client_id)
    port = 1883
    address = "127.0.0.1"
    topic = "#"
    storage = None
    update_screen = None
    should_update = False
    render_thread = None
    pause = True

    def send_data(self, topic: str, value: str, retain: bool):
        self.client.publish(topic, value, retain=retain)

    def pause_screen_update(self):
        self.pause = True
    
    def resume_screen_update(self):
        self.pause = False

    def start_handling(self):
        self.client.loop_start()
        self.render_thread = threading.Thread(target=self.render_loop)
        self.stop_handling_event = threading.Event()

        self.render_thread.start()
    
    def stop_handling(self):
        self.client.loop_stop()
        self.stop_handling_event.set()


    def render_loop(self):
        # update screen every second, if new MQTT messages
        # were recieved in the mean time.
        while(self.stop_handling_event.is_set() == False):
            time.sleep(1)

            if(self.should_update and self.pause == False):
                self.update_screen()
                self.should_update = False

    def add_storage(self, storage_instance):
        self.storage = storage_instance

    def on_message_tree(self, client, userdata, message):
        # remove '' and leading b
        # b'True' -> True
        value = message.payload.decode('utf-8')

        if value == "":
            self.storage.delete(message.topic)
        else:
            self.storage.add(message.topic, value)
        
        self.should_update = True

    def failed_connect(self):
        save_error("Could not connect to " + self.address + ":" + str(self.port))
        save_error("Please ensure a mqtt broker is running.")

    def init(self):
        try:
            self.client.connect(self.address, self.port)
        except Exception:
            self.failed_connect()
            return False
            
        self.client.on_message = self.on_message_tree
        self.client.subscribe(self.topic)

        return True

    def destroy(self):
        self.client.unsubscribe(self.topic)
        self.client.disconnect()
