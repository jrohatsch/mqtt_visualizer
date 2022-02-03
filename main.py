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

pad = curses.newpad(500,50)
# to make the screen re-render when new data arrives
pad.nodelay(True)

pad.scrollok(True)

pad_row_position = 0

last_key = -1
resize_quit = False

# main loop
while(last_key != ord('q')):
    pad.clear()

    pad.addstr("(Press 'q' to close)\n\n")
    pad.addstr("listening to topic: "+ mqtt_handler.topic +"\n")

    try:
        pad.addstr(mqtt_storage.formatted_string(mqtt_storage.data, 0))
    except curses.error:
        pass
    
    try:
        pad.refresh(pad_row_position,0,0,0,curses.LINES - 1,20)
    except curses.error:
        resize_quit = True
        pad.clear()
        break
        
    last_key = pad.getch()

    if last_key == ord('s'):
        pad_row_position += 5
    elif last_key == ord('w'):
        pad_row_position -= 5


mqtt_handler.stop()