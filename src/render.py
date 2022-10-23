import curses
from src.error_handler import *

height_info_box = 5

def init_top_pad():
    return curses.newpad(height_info_box, curses.COLS)

def init_middle_pad():
    return curses.newpad(10000, curses.COLS)

def init_bottom_pad():
    return curses.newpad(1, curses.COLS)

def render_key_info(pad, key: str, info: str):
    try:
        pad.addstr(" " + key + " ", curses.A_STANDOUT)
        pad.addstr(" ")
        pad.addstr(info)
        pad.addstr("  ")
    except Exception as e:
        pad.clear()
        save_error(e)

def update_bottom_pad(pad):
    pad.clear()

    render_key_info(pad, "Q", "Quit")
    render_key_info(pad, "W/A/S/D", "Move Selection")
    render_key_info(pad, "C", "Collapse Tree")

    try:
        pad.refresh(0,0, curses.LINES - 1, 0 , curses.LINES, curses.COLS)
    except Exception as e:
        save_error(e)

def update_info_box(pad, mqtt_handler, mqtt_storage):
    try:
        pad.erase()

        pad.addstr("\n")

        # line 1
        pad.addstr(" ")
        pad.addstr("connected to: " + mqtt_handler.address + ":" + str(mqtt_handler.port) + "\n", curses.A_BOLD)

        # line 2
        pad.addstr(" ")
        pad.addstr("selected topic: " + mqtt_storage.selection_handler.get_selected_string() + "\n", curses.A_BOLD)

        # line 3
        pad.addstr(" ")
        pad.addstr("last update: " + mqtt_storage.selection_handler.get_selected_time() + "\n", curses.A_BOLD)

        pad.box()
        pad.refresh(0, 0, 0, 0, height_info_box, curses.COLS)
    except Exception:
        try:
            pad.clear()
            pad.addstr(" Terminal window too small for info box.\n Please resize and restart.")
            pad.refresh(0, 0, 1, 0, height_info_box, curses.COLS)
        except Exception as e:
            save_error(e)


def update_content_box(pad, mqtt_storage, pad_row_position):

    def render_func(text, parent_ref = None, style = curses.A_NORMAL):
        pad.addstr(" ")
        pad.addstr(text, style)

        if(parent_ref != None and 
            parent_ref.get("sub_topics") != None and 
            parent_ref.get("sub_topics").get(text) != None):
            parent_ref.get("sub_topics").get(text)["coordinates"] = pad.getyx()

        

    pad.erase()
    mqtt_storage.render_formatted_string(render_func, mqtt_storage.data)

    try:
        #pad.box()
        pad.refresh(pad_row_position, 0, height_info_box, 0, curses.LINES - 2, curses.COLS)
    except Exception as e:
        save_error(e)


