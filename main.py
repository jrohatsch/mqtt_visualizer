import locale
import curses
from storage import Storage
from mqtt_handler import MqttHandler
import arguments


# read arguments
args = arguments.get()


mqtt_storage = Storage()
mqtt_handler = MqttHandler()
mqtt_handler.add_storage(mqtt_storage)

# set address and topic from args 
if args.address != None:
    mqtt_handler.address = args.address
if args.topic != None:
    mqtt_handler.topic = args.topic

mqtt_handler.init()
window = curses.initscr()
locale.setlocale(locale.LC_ALL, '')

# make cursor invisible
curses.curs_set(0)

pad = curses.newpad(500,90)
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
top_pad.refresh(0,0,0,0,4, curses.COLS - 1)

mqtt_handler.client.loop_start()
# main loop
while(last_key != ord('q')):
    pad.clear()

    pad.addstr(mqtt_storage.formatted_string(mqtt_storage.data, 0))
    pad.addstr("\n\n--------------------------------------------")

    try:
        pad.refresh(pad_row_position, 0, 4, 0, curses.LINES - 1, curses.COLS - 1)
    except curses.error:
        break
        
    last_key = pad.getch()

    if last_key == ord('s'):
        pad_row_position += 5
    elif last_key == ord('w'):
        pad_row_position -= 5

# after main loop on quit or error
mqtt_handler.client.loop_stop()
curses.endwin()
print("program exited")
mqtt_handler.destroy()