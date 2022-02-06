import locale
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

# add top section
top_pad = curses.newpad(4,90)
top_pad.clear()
    
top_pad.addstr("(Press 'q' to close, 'w' and 's' to sroll up or down.)\n\n")
top_pad.addstr("listening to topic: "+ mqtt_handler.topic +"\n")
top_pad.addstr("--------------------------------------------");
top_pad.refresh(0,0,0,0,4,90)

# main loop
while(last_key != ord('q')):
    pad.clear()

    try:
        pad.addstr(mqtt_storage.formatted_string(mqtt_storage.data, 0))
    except curses.error:
        pass
    
    try:
        pad.refresh(pad_row_position,0,4,0,curses.LINES - 1,20)
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