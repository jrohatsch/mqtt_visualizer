# mqtt_visualizer
Visualize MQTT data traffic in a terminal.

![](https://github.com/jrohatsch/media_store/blob/master/mqtt_demo.gif)

## Run the app

### Unix based systems

Use python up to version 3.10.2

Install following modules

```pip3 install paho-mqtt```

Run 

```python3 mqtt_visualizer.py```

to start the program and connect to the local mqtt broker 127.0.0.1.

### Docker

build the image

```docker build -t mqtt_visualizer .```

run the image

```docker run -it --rm mqtt_visualizer```


## Packaged builds
[macOS](https://github.com/jrohatsch/mqtt_visualizer/blob/main/builds/macOS-12.6-arm64.zip)
[Linux](https://github.com/jrohatsch/mqtt_visualizer/blob/main/builds/Linux.zip)

## Before Starting

Make sure there is a mqtt broker running to the connecting machine (for example [mosquitto](https://mosquitto.org/)).

When connecting to a remote computer with -a argument, make sure the specified port is not blocked by a firewall.
Also the mqtt-broker must allow connections from non-local machines. To enable any machines with mosquitto add these lines
to the config file:

```
listener 1883
allow_anonymous true
```

## Keyboard Bindings

| key | action |
----------|------------|
q    | quit the app
w    | move selection to topic above
a    | move selection to parent topic
s    | move selection to topic below
d    | move selection to child topics
c    | collapse child topics of selected topic

## Arguments

| argument | description | default value
|----------|------------|---|
| -a | ip adress to the MQTT Broker| "127.0.0.1"
| -p | port number to use | 1883
| -t | topic to which to subscribe to| "#"

### examples

```python3 mqtt_visualizer.py -a 127.0.0.1 -t main/+/temp```

will connect to localhost on topic main/+/temp.

