import curses


class Storage():
    data = {"value": "", "sub_topics": {}}

    def add(self, path, value):
        path_array = str(path).split("/")

        # helper referece to iterate the data dictionary
        help = self.data["sub_topics"]

        i = 0
        for path in path_array:
            # create empty dictionary
            if not path in help:
                help[path] = {"value": "", "sub_topics": {}}
            
            # set value
            if(i == len(path_array) - 1):
                help[path]["value"] = value

            help = help[path]["sub_topics"]
            i = i + 1

                
    def formatted_string(self, data, level):
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

        # copy list before iteration
        items = list(data.get("sub_topics").items())
        
        for key, value in items:
            render_func("\n")
            
            for i in range(level):
                render_func("  ")

            render_func(key, curses.A_BOLD)
            self.render_formatted_string(render_func, value, level + 1)

