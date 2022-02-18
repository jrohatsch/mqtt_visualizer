
def print_string(data):
    success = False

    try:
        with open('data.log', 'w') as f:
            f.write(data)
        
        success = True
    except:
        success = False
    
    return success

