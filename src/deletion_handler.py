

def remove_dead_entries(data: dict, path_array: list, selection_handler, index: int = 1):
    if index == len(path_array):
        return

    # check if entry has no sub_topics any more
    if len(data.get("sub_topics")) == 0:
        # check if entry has no value
        if data.get("value") == "":
            # save ref of parent
            parent = data.get("parent_ref")

            if parent != None:
                # if the dead entry was selected
                # set selection to parent entry
                if data.get("selected") == True:
                    selection_handler.set_selection_to_parent()

                # remove dead entry
                parent.get("sub_topics").pop(
                path_array[len(path_array) - index])
                
                # repeat for parent  entry
                remove_dead_entries(parent, path_array, selection_handler, index + 1)
