import argparse

parser = argparse.ArgumentParser(description='Connection Details')

parser.add_argument('-a',dest='address',help='The ip address to which the mqtt_visualizer should connect', type=str, default="127.0.0.1")
parser.add_argument('-p',dest='port',help='The port to which the mqtt_visualizer should connect', type=int, default=1883)
parser.add_argument('-t',dest='topic', help='the mqtt topic which should be observed', type=str, default="#")
parser.add_argument('--docker',dest='docker', help='boolean flag wether the app run through docker', type=bool, default=False)

def get():
    return parser.parse_args()