import os, sys

# assume python is run from mqtt_visualizer
# add this path of the parent dir
dir = os.path.abspath('.')
sys.path.append(dir)


from storage import Storage
import print_file

test_storage = Storage()

test_storage.add("main/sub","valueString")
test_storage.add("main/sub2", "123")
test_storage.add("main/sub3", "true")

test_string = test_storage.formatted_string(test_storage.data)
print_file.print_string(test_string)

