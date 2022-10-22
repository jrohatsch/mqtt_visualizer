import locale
import curses
from src.storage import Storage
from src.mqtt_handler import MqttHandler
from src.error_handler import *
import src.arguments as arguments
from src.render import *


def main(window):
    # read arguments
    args = arguments.get()

    mqtt_storage = Storage()
    mqtt_handler = MqttHandler()
    mqtt_handler.add_storage(mqtt_storage)

    # set address and topic from args 
    mqtt_handler.address = args.address
    mqtt_handler.topic = args.topic
    mqtt_handler.port = args.port

    # if app is run through docker replace localhost
    if(args.docker == True and args.address == "127.0.0.1"):
        mqtt_handler.address = "host.docker.internal"

    success = mqtt_handler.init()

    if not success:
        return 0

    locale.setlocale(locale.LC_ALL, '')

    # make cursor invisible
    curses.curs_set(0)

    pad = curses.newpad(10000, curses.COLS - 1)

    pad_row_position = 0
    last_key = ""

    # add top section
    top_pad = curses.newpad(6, curses.COLS - 1)
    update_info_box(top_pad, mqtt_handler, mqtt_storage)

    # pass update function to mqtt handler
    def update_screen():
        update_content_box(pad, mqtt_storage, pad_row_position)
        update_info_box(top_pad,mqtt_handler,mqtt_storage)
    
    mqtt_handler.update_screen = update_screen

    # mqtt loop:
    # start mqtt handling in separate thread
    # to ensure screen is only updated when
    # new data arrives
    mqtt_handler.start_handling()
    
    # key press loop:
    # wait for user input and update the screen
    while last_key.upper() != 'Q':
        update_screen()
        # after processing key press, resume updates on new data
        mqtt_handler.resume_screen_update()

        try:
            # wait for key press
            last_key = pad.getkey()
        except KeyboardInterrupt:
            pass

        # while processing key press, pause updates on new data
        mqtt_handler.pause_screen_update()

        if last_key.upper() in "WASD":
            if last_key.upper() == 'D':
                mqtt_storage.selection_handler.update_selection("into_tree")
            elif last_key.upper() == 'S':
                mqtt_storage.selection_handler.update_selection("down")
            elif last_key.upper() == 'A':
                mqtt_storage.selection_handler.update_selection("to_parent")
            elif last_key.upper() == 'W':
                mqtt_storage.selection_handler.update_selection("up")
            
            # scroll if selection is in bottom half of terminal screen
            if(mqtt_storage.selection_handler.get_selected_ref() != None and mqtt_storage.selection_handler.get_selected_ref().get("coordinates") != None):
                pad_row_position = mqtt_storage.selection_handler.get_selected_ref().get("coordinates")[0] - ((curses.LINES - height_info_box) // 2)
            
            update_info_box(top_pad, mqtt_handler, mqtt_storage)
        elif last_key.upper() == 'C':
            mqtt_storage.selection_handler.collapse()
        elif last_key == 'KEY_RESIZE':
            # if terminal window resize was registered
            curses.resize_term(window.getmaxyx()[0], window.getmaxyx()[1])
            top_pad = curses.newpad(8, curses.COLS - 1)
            pad = curses.newpad(10000, curses.COLS - 1)

            update_info_box(top_pad, mqtt_handler, mqtt_storage)
            update_screen()

    # exit the app
    top_pad.clear()
    pad.clear()
    mqtt_handler.stop_handling()
    mqtt_handler.destroy()
    curses.endwin()


curses.wrapper(main)
