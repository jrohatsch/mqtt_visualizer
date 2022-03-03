# mqtt_visualizer
Visualize MQTT data traffic in a terminal.

![](https://github.com/jrohatsch/media_store/blob/master/mqtt_demo.gif)

## Installation

### Unix based systems

Use python up to version 3.10.2

Install following modules

```pip3 install paho-mqtt```

### Windows

Use python up to version 3.10.2

Install following modules

```pip3 install paho-mqtt windows-curses```

## Usage
### Before Starting

Make sure there is a mqtt broker running to the connecting machine (for example [mosquitto](https://mosquitto.org/)).

When connecting to a remote computer with -a argument, make sure the specified port is not blocked by a firewall.

### Starting

Run 

```python3 main.py```

to start the program and connect to the local mqtt broker 127.0.0.1.

### Keyboard Bindings

| key | action |
----------|------------|
w    | move selection to topic above
s    | move selection to topic below
a    | move selection to parent topic
d    | move selection to child topics
c    | collapse child topics of selected topic
i    | scroll screen up
k    | scroll screen down
p    | print mqtt data tree to .log file

### Arguments

| argument | description | default value
|----------|------------|---|
| -a | ip adress to the MQTT Broker| "127.0.0.1"
| -p | port number to use | 1883
| -t | topic to which to subscribe to| "#"
