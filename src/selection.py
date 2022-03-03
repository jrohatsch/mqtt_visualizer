
class SelectionHandler():
    __ref_selected_topic = None

    def set_selected_ref(self, reference_topic):
        self.__ref_selected_topic = reference_topic

    def get_selected_ref(self):
        return self.__ref_selected_topic

    def get_selected_string(self):
        if(self.__ref_selected_topic == None):
            return ""
        else:
            return self.__ref_selected_topic.get("path")


    def set_selection_to_parent(self):
        selected_topic = self.__ref_selected_topic
        parent = selected_topic.get("parent_ref")

        if(parent.get("path") != "#"):
            selected_topic["selected"] = False
            parent["selected"] = True
            self.__ref_selected_topic = parent


    def set_selection_to_sister(self, delta: int):
        selected_topic = self.__ref_selected_topic

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
        self.__ref_selected_topic = sister


    def set_selection_to_first_child(self):
        selected_topic = self.__ref_selected_topic

        # ensure sub_topics are shown
        if(selected_topic.get("show_sub_topics") == True and len(selected_topic.get("sub_topics")) > 0):
            selected_topic["selected"] = False

            sub_topics = list(selected_topic.get("sub_topics").values())

            sub_topics[0]["selected"] = True
            self.__ref_selected_topic = sub_topics[0]


    def expand(self):
        if(self.__ref_selected_topic != None):
            self.__ref_selected_topic["show_sub_topics"] = True


    def collapse(self):
        if(self.__ref_selected_topic != None):
            self.__ref_selected_topic["show_sub_topics"] = False


    def update_selection(self, direction):
        if self.__ref_selected_topic == None:
            return
        if (direction == "into_tree"):
            self.expand()
            self.set_selection_to_first_child()
        elif (direction == "down"):
            self.set_selection_to_sister(1)
        elif (direction == "up"):
            self.set_selection_to_sister(-1)
        elif (direction == "to_parent"):
            self.set_selection_to_parent()
