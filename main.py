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
code = locale.getpreferredencoding()
curses.curs_set(2)

# to make the screen re-render when new data arrives
window.nodelay(True)


last_key = -1
# main loop
while(last_key != ord('q')):
    window.clear()
    topleft = window.getbegyx()

    window.addstr("Data: \n")
    window.addstr(str(mqtt_storage.data) + "\n")
    last_key = window.getch()
    window.refresh()

mqtt_handler.stop()