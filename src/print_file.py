import datetime 
import os.path
from src.error_handler import *

# save errors for after quitting

def print_string(data):
    success = False
    
    file_name = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    file_name += ".log"

    try:
        with open("logs/" + file_name, "w") as f:
            f.write(data)
        
        success = True
    except Exception as e:
        success = False
        save_error(e)

    
    # check if file was written
    exists = os.path.exists("logs/" + file_name)

    if (exists and success):
        return "-> " + file_name
    else:
        return " print failed"

