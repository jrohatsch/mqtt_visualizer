import locale
import curses
from src.storage import Storage
from src.mqtt_handler import MqttHandler
from src.print_file import print_string
from src.error_handler import *
import src.arguments as arguments
from src.render import *


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
    top_pad = curses.newpad(8, curses.COLS - 1)
    update_info_box(top_pad, print_status, mqtt_handler, mqtt_storage)

    # pass update function to mqtt handler
    def update_screen():
        update_content_box(pad, mqtt_storage, pad_row_position)
    
    mqtt_handler.update_screen = update_screen

    # mqtt loop:
    # start mqtt handling in separate thread
    # to ensure screen is only updated when
    # new data arrives
    mqtt_handler.start_handling()
    
    # key press loop:
    # wait for user input and update the screen
    while(last_key != ord('q')):
        update_screen()
        # after processing key press, resume updates on new data
        mqtt_handler.resume_screen_update()

        # wait for key press
        last_key = pad.getch()

        # while processing key press, pause updates on new data
        mqtt_handler.pause_screen_update()

        if last_key == ord('k'):
            if (pad_row_position <= 9995):
                pad_row_position += 5
            else:
                pad_row_position = 10000
        elif last_key == ord('i'):
            if (pad_row_position >= 5):
                pad_row_position -= 5
            else:
                pad_row_position = 0
        elif last_key == ord('p'):
            print_status = print_string(mqtt_storage.formatted_string(mqtt_storage.data))
            update_info_box(top_pad, print_status, mqtt_handler, mqtt_storage)
        elif last_key == ord('d'):
            mqtt_storage.selection_handler.update_selection("into_tree")
            update_info_box(top_pad, print_status, mqtt_handler, mqtt_storage)
        elif last_key == ord('s'):
            mqtt_storage.selection_handler.update_selection("down")
            update_info_box(top_pad, print_status, mqtt_handler, mqtt_storage)
        elif last_key == ord('a'):
            mqtt_storage.selection_handler.update_selection("to_parent")
            update_info_box(top_pad, print_status, mqtt_handler, mqtt_storage)
        elif last_key == ord('w'):
            mqtt_storage.selection_handler.update_selection("up")
            update_info_box(top_pad, print_status, mqtt_handler, mqtt_storage)
        elif last_key == ord('c'):
            mqtt_storage.selection_handler.collapse()
        elif last_key == curses.KEY_RESIZE:
            # if terminal window resize was registered
            curses.resize_term(window.getmaxyx()[0], window.getmaxyx()[1])
            top_pad = curses.newpad(8, curses.COLS - 1)
            pad = curses.newpad(10000, curses.COLS - 1)

            update_info_box(top_pad, print_status, mqtt_handler, mqtt_storage)
            update_screen()

    
    top_pad.clear()
    pad.clear()
    mqtt_handler.stop_handling()
    mqtt_handler.destroy()
    curses.endwin()


main()

# after main loop on quit or error
#print_errors()
print("program exited")
