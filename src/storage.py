import curses
import time
from src.error_handler import save_error
from src.selection import SelectionHandler
from src.deletion_handler import remove_dead_entries

class Storage():
    data = {
        "value": "",
        "sub_topics": {},
        "show_sub_topics": True,
        "selected": False,
        "parent_ref": None,
        "path": "#",
        "date": None,
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
            for j in range(i + 1):
                if(sub_path != ""):
                    sub_path += "/"
                sub_path += path_array[j]

            # create empty dictionary
            if not path in help:
                help[path] = {
                    "value": "",
                    "sub_topics": {},
                    "show_sub_topics": False,
                    "selected": False,
                    "parent_ref": parent,
                    "path": sub_path,
                    "date": time.time()
                }

            # set value
            if(i == len(path_array) - 1):
                help[path]["value"] = value
                help[path]["date"] = time.time()

            parent = help[path]
            help = help[path]["sub_topics"]
            i = i + 1

        # if first entry, set selected flag
        if (self.selection_handler.get_selected_ref() == None):
            self.data["sub_topics"][path_array[0]]["selected"] = True
            self.selection_handler.set_selected_ref(
                self.data["sub_topics"][path_array[0]])

    def delete(self, full_path: str):
        # find data
        path_array = str(full_path).split("/")

        # helper referece to iterate the data dictionary
        help = self.data

        # iterate to the parent element
        for path in path_array[:-1]:

            if not path in help.get("sub_topics"):
                break
            

            help = help.get("sub_topics").get(path)
        
        # remove element
        try:
            entry_to_delete = help.get("sub_topics")[path_array[len(path_array) - 1]]
        except KeyError:
            save_error("key already deleted " + full_path)
            return

        # check if entry has sub topics
        if len(entry_to_delete.get("sub_topics")) > 0:
            # just overwrite value with empty string
            entry_to_delete["value"] = ""
        else:
            # check if entry was selected
            # set selection to parent entry
            if entry_to_delete.get("selected") == True:
                self.selection_handler.set_selection_to_parent()

            # remove complete entry
            help.get("sub_topics").pop(path_array[len(path_array) - 1])

            remove_dead_entries(help, path_array[:-1], self.selection_handler)


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
            render_func(text=" = ", parent_ref=data.get("parent_ref"), style=curses.A_BOLD)
            render_func(text=data.get("value"),parent_ref=data.get("parent_ref"))
        
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

                render_func(text=key, style=style, parent_ref=value.get("parent_ref"))

                self.render_formatted_string(render_func, value, level + 1)
    






        









    

