import curses
from src.selection import SelectionHandler

class Storage():
    data = {
        "value": "", 
        "sub_topics": {}, 
        "show_sub_topics": True, 
        "selected": False, 
        "parent_ref": None, 
        "path": "#"
    }

    selection_handler = SelectionHandler()

    def add(self, full_path: str, value: str):
        path_array = str(full_path).split("/")

        # helper referece to iterate the data dictionary
        parent = self.data
        help = self.data["sub_topics"]

        i = 0
        for path in path_array:

            # create subpath to topic
            sub_path = ""
            for j in range (i + 1):
                sub_path += path_array[j]
                sub_path += "/"

            # create empty dictionary
            if not path in help:
                help[path] = {
                    "value": "", 
                    "sub_topics": {}, 
                    "show_sub_topics": False, 
                    "selected": False, 
                    "parent_ref": parent, 
                    "path": sub_path
                }
            
            # set value
            if(i == len(path_array) - 1):
                help[path]["value"] = value

            parent = help[path]
            help = help[path]["sub_topics"]
            i = i + 1
        
        # if first entry, set selected flag
        if (self.selection_handler.get_selected_ref() == None):
            self.data["sub_topics"][path_array[0]]["selected"] = True
            self.selection_handler.set_selected_ref(self.data["sub_topics"][path_array[0]])

                
    def formatted_string(self, data, level = 0):
        buffer = ""

        if(data.get("value") != ""):
            buffer += " = " + data.get("value")
        

        for key, value in data.get("sub_topics").items():
            buffer += "\n"
            
            for i in range(level):
                buffer += "  "

            buffer += key
            buffer += self.formatted_string(value, level + 1)

        return buffer

    def render_formatted_string(self, render_func, data, level = 0):
        if(data.get("value") != ""):
            render_func(" = ", curses.A_BOLD)
            render_func(data.get("value"))
        
        # check if data has sub_topics
        if (len(data.get("sub_topics")) > 0 and data.get("show_sub_topics") == False):
            render_func(" [+]")

        if(data.get("show_sub_topics") == True):
            # copy list before iteration
            items = list(data.get("sub_topics").items())
            
            for key, value in items:
                render_func("\n")
                
                for i in range(level):
                    render_func("  ")

                style = curses.A_BOLD

                if(value.get("selected") == True):
                    style = curses.A_STANDOUT

                render_func(key, style)

                self.render_formatted_string(render_func, value, level + 1)
    






        









    

