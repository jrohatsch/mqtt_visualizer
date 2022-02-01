import locale
import time
import curses
from storage import Storage
from mqtt_handler import MqttHandler


mqtt_storage = Storage()
mqtt_handler = MqttHandler()
mqtt_handler.add_storage(mqtt_storage)

mqtt_handler.init()
mqtt_handler.start()

window = curses.initscr()
locale.setlocale(locale.LC_ALL, '')

# make cursor invisible
curses.curs_set(0)

# to make the screen re-render when new data arrives
window.nodelay(True)

window.scrollok(True)

last_key = -1
# main loop
while(last_key != ord('q')):
    window.clear()

    window.addstr("(Press 'q' to close)\n\n")
    window.addstr("listening to topic: "+ mqtt_handler.topic +"\n")

    try:
        window.addstr(mqtt_storage.formatted_string(mqtt_storage.data, 0))
    except curses.error:
        pass
    
    window.refresh()
    time.sleep(1)
    last_key = window.getch()

mqtt_handler.stop()