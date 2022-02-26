import curses

class Storage():
    data = {
        "value": "", 
        "sub_topics": {}, 
        "show_sub_topics": True, 
        "selected": False, 
        "parent_ref": None, 
        "path": "#"
    }
    ref_selected_topic = None

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
        if (self.ref_selected_topic == None):
            self.data["sub_topics"][path_array[0]]["selected"] = True
            self.ref_selected_topic = self.data["sub_topics"][path_array[0]]

                
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
    
    def expand(self):
        selected_topic = self.ref_selected_topic

        if(selected_topic != None):
            selected_topic["show_sub_topics"] = True
    
    def collapse(self):
        selected_topic = self.ref_selected_topic

        if(selected_topic != None):
            selected_topic["show_sub_topics"] = False

    def __set_selection_to_first_child(self):
        selected_topic = self.ref_selected_topic

        # ensure sub_topics are shown
        if(selected_topic.get("show_sub_topics") == True and len(selected_topic.get("sub_topics")) > 0):
            selected_topic["selected"] = False

            sub_topics = list(selected_topic.get("sub_topics").values())

            sub_topics[0]["selected"] = True
            self.ref_selected_topic = sub_topics[0]

    def __set_selection_to_sister(self, delta):
        selected_topic = self.ref_selected_topic

        parent = selected_topic.get("parent_ref")

        sub_topics = list(parent.get("sub_topics").values())

        selected_topic_index = 0

        i = 0
        for sub_topic in sub_topics:
            if(selected_topic.get("path") == sub_topic.get("path")):
                selected_topic_index = i
            i = i + 1 
        

        sister_index = selected_topic_index + delta

        if delta > 0:
            # check if index is at end
            if(selected_topic_index == len(sub_topics) - 1):
                sister_index = 0
        else:
            # check if index is at start
            if(selected_topic_index == 0):
                sister_index = len(sub_topics) - 1
            

        sister = sub_topics[sister_index]

        selected_topic["selected"] = False
        sister["selected"] = True
        self.ref_selected_topic = sister

    def __set_selection_to_parent(self):
        selected_topic = self.ref_selected_topic
        parent = selected_topic.get("parent_ref")

        if(parent.get("path") != "#"):
            selected_topic["selected"] = False
            parent["selected"] = True
            self.ref_selected_topic = parent
        
    def update_selection(self, direction):
        if (direction == "into_tree"):
            self.expand()
            self.__set_selection_to_first_child()
        elif (direction == "down"):
            self.__set_selection_to_sister(1)
        elif (direction == "up"):
            self.__set_selection_to_sister(-1)
        elif (direction == "to_parent"):
            self.__set_selection_to_parent()

    def get_selected(self):
        if(self.ref_selected_topic == None):
            return ""
        else:
            return self.ref_selected_topic.get("path")






    

