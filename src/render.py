import curses
from src.error_handler import *

height_info_box = 9

def render_key_info(pad, key: str, info: str):
    pad.addstr(" " + key + " ", curses.A_STANDOUT)
    pad.addstr(" ")
    pad.addstr(info)
    pad.addstr("  ")


def update_info_box(pad, print_status, mqtt_handler, mqtt_storage):
    try:
        pad.erase()

        pad.addstr("\n")

        # line 1
        pad.addstr(" ")
        render_key_info(pad, "Q", "Close")
        render_key_info(pad, "W", "Move Select Up")
        render_key_info(pad, "S", "Move Select Down")
        render_key_info(pad, "E", "Edit Data")
        pad.addstr("\n")

        # line 2
        pad.addstr(" ")
        render_key_info(pad, "A", "Move Select to Parent")
        render_key_info(pad, "D", "Move Select to Child")
        render_key_info(pad, "C", "Collapse Tree")
        pad.addstr("\n")

        # line 3
        pad.addstr(" ")
        render_key_info(pad, "I", "Scroll Up")
        render_key_info(pad, "K", "Scroll Down")
        render_key_info(pad, "P", "Print")
        pad.addstr(print_status)
        pad.addstr("\n\n")

        # line 4
        pad.addstr(" ")
        pad.addstr("connected to: " + mqtt_handler.address + ":" + str(mqtt_handler.port) + "\n", curses.A_BOLD)

        # line 5
        pad.addstr(" ")
        pad.addstr("selected topic: " + mqtt_storage.selection_handler.get_selected_string() + "\n", curses.A_BOLD)

        pad.box()
        pad.refresh(0, 0, 1, 0, height_info_box, curses.COLS - 1)
    except Exception:
        try:
            pad.clear()
            pad.addstr(" Terminal window too small for info box.\n Please resize and restart.")
            pad.refresh(0, 0, 1, 0, height_info_box, curses.COLS - 1)
        except Exception as e:
            save_error(e)


def update_content_box(pad, mqtt_storage, pad_row_position):

    def render_func(text, option = curses.A_NORMAL):
        pad.addstr(" ")
        pad.addstr(text, option)

    pad.erase()
    mqtt_storage.render_formatted_string(render_func, mqtt_storage.data)

    try:
        pad.box()
        pad.refresh(pad_row_position, 0, height_info_box, 0, curses.LINES - 1, curses.COLS - 1)
    except Exception as e:
        save_error(e)

def is_valid(key):
    if key == None:
        return False

    alphabet = "abcdefghijklmnopqrstuvwxyzäöü/_-0123456789"

    return key in alphabet

def update_send_data_box(pad, mqtt_handler, selected_topic):
    curses.curs_set(1)

    pad.clear()
    pad.box()
    pad.addstr(1,1,"Publish data")
    pad.addstr(2,1,"Topic:")

    # get topic string

    topic_string = selected_topic[:-1]
    last_key = None
    while last_key != '\n':
        filler = ''
        if last_key != None and ord(last_key) == 127:
            topic_string = topic_string[:-1]
            filler = ' '
        elif is_valid(last_key):
            topic_string += last_key
        
        pad.addstr(3,1,topic_string+filler)
        pad.refresh(0, 0, 1, 0, height_info_box, curses.COLS - 1)
        try:
            last_key = pad.getkey()
        except KeyboardInterrupt:
            curses.curs_set(0)
            return
    
    # get value string

    pad.addstr(4,1,"Data")
    pad.move(5,1)
    value_string = ''
    last_key = None
    while last_key != '\n':
        if last_key != None and ord(last_key) == 127:
            value_string = value_string[:-1]
            pad.addstr(5,1,value_string+" ")
        elif last_key != None:
            value_string += last_key
            pad.addstr(5,1,value_string)
        pad.refresh(0, 0, 1, 0, height_info_box, curses.COLS - 1)
        try:
            last_key = pad.getkey()
        except KeyboardInterrupt:
            curses.curs_set(0)
            return

    # get retain flag
            
    retain = None

    pad.addstr(6,1,"Retain? (Y/N)")
    pad.refresh(0, 0, 1, 0, height_info_box, curses.COLS - 1)

    last_key = pad.getkey()

    if last_key.upper() == 'Y':
        retain = True
    elif last_key.upper() == 'N':
        retain = False
        

    mqtt_handler.send_data(topic=topic_string, value=value_string, retain=retain)

    curses.curs_set(0)
    


