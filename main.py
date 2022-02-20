import locale
import curses
from storage import Storage
from mqtt_handler import MqttHandler
from print_file import print_string
from error_handler import *
import arguments
import time

def render_top_pad(top_pad, print_status, mqtt_handler):
    top_pad.erase()
        
    top_pad.addstr("Press 'q' to close, 'w' and 's' to sroll up or down.\n", curses.A_STANDOUT)
    top_pad.addstr("Press 'p' to print to file. " + print_status +"\n\n", curses.A_STANDOUT)
    top_pad.addstr("connected to: " + mqtt_handler.address + ":" + str(mqtt_handler.port) + "\n", curses.A_BOLD)
    top_pad.addstr("listening to topic: "+ mqtt_handler.topic +"\n", curses.A_BOLD)
    top_pad.addstr("--------------------------------------------",curses.A_BOLD);
    top_pad.refresh(0,0,0,0,6, curses.COLS - 1)


def main():
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
    if args.port != None:
        mqtt_handler.port = args.port

    success = mqtt_handler.init()

    if not success:
        return 0
    
    window = curses.initscr()

    locale.setlocale(locale.LC_ALL, '')

    # make cursor invisible
    curses.curs_set(0)

    pad = curses.newpad(10000, curses.COLS - 1)

    pad_row_position = 0
    last_key = -1

    print_status = ""

    # add top section
    top_pad = curses.newpad(7, curses.COLS - 1)
    render_top_pad(top_pad, print_status, mqtt_handler)

    def update_screen():
        pad.erase()
        mqtt_storage.render_formatted_string(pad.addstr, mqtt_storage.data)
        pad.addstr("\n\n--------------------------------------------", curses.A_BOLD)

        try:
            pad.refresh(pad_row_position, 0, 6, 0, curses.LINES - 1, curses.COLS - 1)
        except Exception as e:
            save_error(e)
    
    mqtt_handler.update_screen = update_screen

    # mqtt loop:
    # start mqtt handling in separate thread
    # to ensure screen is only updated when
    # new data arrives
    mqtt_handler.client.loop_start()
    
    # curses loop:
    # wait for user input and update screen
    # after recieving an input
    while(last_key != ord('q')):
        update_screen()
            
        # this function is blocking
        last_key = pad.getch()

        if last_key == ord('s'):
            if (pad_row_position <= 9995):
                pad_row_position += 5
            else:
                pad_row_position = 10000
        elif last_key == ord('w'):
            if (pad_row_position >= 5):
                pad_row_position -= 5
            else:
                pad_row_position = 0
        elif last_key == ord('p'):
            print_status = print_string(mqtt_storage.formatted_string(mqtt_storage.data))
            render_top_pad(top_pad, print_status, mqtt_handler)
        

    mqtt_handler.client.loop_stop()
    mqtt_handler.destroy()
    curses.endwin()



main()

# after main loop on quit or error
print_errors()
print("program existed")
