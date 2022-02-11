import argparse

from numpy import number

parser = argparse.ArgumentParser(description='Connection Details')

parser.add_argument('-a',dest='address',help='The ip address to which the mqtt_visualizer should connect', type=str)
parser.add_argument('-p',dest='port',help='The port to which the mqtt_visualizer should connect', type=number)
parser.add_argument('-t',dest='topic', help='the mqtt topic which should be observed', type=str)

def get():
    return parser.parse_args()