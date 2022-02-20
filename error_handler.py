errors = []

def save_error(e):
    errors.append(e)

def print_errors():
    for e in errors:
        print(e)