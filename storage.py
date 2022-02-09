from xml.dom.expatbuilder import parseString


class Storage():
    data = {}

    def add(self, path, value):
        path_array = str(path).split("/")

        # helper referece to iterate the data dictionary
        help = self.data

        for i in range(len(path_array) - 1):
            path = path_array[i]

            # create sub dictionary if it not exists
            if not path in help:
                help[path] = {}

            help = help[path]

        # add value at deepest level
        help[path_array[len(path_array) - 1]] = value

    def formatted_string(self, data, level):
        buffer = ""

        try:
            keys = data.keys()
            for key in keys:
                buffer += "\n"
                #buffer += "level"+str(level)+"\n"
                for i in range(level):
                    buffer += "  "

                buffer += key
                buffer += self.formatted_string(data.get(key), level + 1)
        except AttributeError:
            # at deepest level. data is not a dictionary
            buffer += " = "
            buffer += data

        return buffer
