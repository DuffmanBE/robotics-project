import socket
import pickle
import struct
from enum import Enum

from sense_hat import SenseHat


# send(s, {"action": "move_pixel", "payload": Action.DOWN})
class Action(Enum):
    NOTHING = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


current_led = [4, 4]


def set_pixel(x, y):
    sense.clear()
    if x > -1 and x < 8 and y > -1 and y < 8:
        sense.set_pixel(x, y, 255, 0, 0)
    global current_led
    current_led = [x, y]
    print("Current-led in set pixel:")
    print(current_led)


def recv(s):
    global current_led
    data = s.recv(4, socket.MSG_WAITALL)
    data_len = struct.unpack('>i', data)[0]
    data = pickle.loads(s.recv(data_len, socket.MSG_WAITALL))
    print("Received data!", data)
    if 'action' in data:
        if data["action"] == "set_pixel":
            coordinates = data["payload"]
            set_pixel(coordinates[0], coordinates[1])
        elif data["action"] == "move_pixel":
            action = data["payload"]
            if action == Action.NOTHING:
                print("Nothing action")
            elif action == Action.DOWN:
                set_pixel(current_led[0], current_led[1] - 1)
            elif action == 2:
                print("Current-led in set down:")
                print(current_led)
                set_pixel(current_led[0], current_led[1] + 1)
            elif action == 3:
                set_pixel(current_led[0] - 1, current_led[1])
            elif action == 4:
                set_pixel(current_led[0] + 1, current_led[1])

    o = sense.get_orientation()
    acceleration = sense.get_accelerometer_raw()
    pitch = o["pitch"]
    roll = o["roll"]
    yaw = o["yaw"]
    x = acceleration["x"]
    y = acceleration["y"]
    z = acceleration["z"]

    s.sendall(pickle.dumps({
        "orientation": {
            "pitch": pitch,
            "roll": roll,
            "yaw": yaw
        },
        "accelerometer": {
            "x": x,
            "y": y,
            "z": z
        }
    }))


# Create server

sense = SenseHat()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 9395))
s.listen(10)

while True:
    # Accept a client
    print("Hello world!")
    conn, addr = s.accept()
    while True:
        recv(conn)


