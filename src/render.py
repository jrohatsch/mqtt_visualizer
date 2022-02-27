import curses
from src.error_handler import *

height_info_box = 8

def update_info_box(pad, print_status, mqtt_handler, mqtt_storage):
    pad.erase()

    pad.addstr("Press 'q' to close, 'w' and 's' to move selection up and down.\n", curses.A_STANDOUT)
    pad.addstr("Press 'a' to move selection to the parent topic. Press 'd' to open sub topics.\n", curses.A_STANDOUT)
    pad.addstr("Press 'c' to collapse topic trees.\n", curses.A_STANDOUT)
    pad.addstr("Press 'i' and 'k' to scroll the screen up and down.\n", curses.A_STANDOUT)
    pad.addstr("Press 'p' to print to file." + print_status + "\n", curses.A_STANDOUT)
    pad.addstr("connected to: " + mqtt_handler.address + ":" + str(mqtt_handler.port) + "\n", curses.A_BOLD)
    pad.addstr("selected topic: " + mqtt_storage.selection_handler.get_selected_string() + "\n", curses.A_BOLD)
    pad.addstr("--------------------------------------------", curses.A_BOLD)
    pad.refresh(0, 0, 0, 0, height_info_box, curses.COLS - 1)


def update_content_box(pad, mqtt_storage, pad_row_position):
    pad.erase()
    mqtt_storage.render_formatted_string(pad.addstr, mqtt_storage.data)
    pad.addstr("\n\n--------------------------------------------", curses.A_BOLD)

    try:
        pad.refresh(pad_row_position, 0, height_info_box, 0, curses.LINES - 1, curses.COLS - 1)
    except Exception as e:
        save_error(e)
