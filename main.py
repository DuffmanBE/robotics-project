import socket
import pickle
import struct
from enum import Enum
import cv2
import numpy as np


class Action(Enum):
    NOTHING = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Socket:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.s.connect(('192.168.0.218', 9395))

    def getSocket(self):
        return self.s


class AgentController():
    def __init__(self, socket):
        self.s = socket
        self.send({"action": "set_pixel", "payload": (0, 0)})

    def send(self, data):
        data = pickle.dumps(data)
        self.s.sendall(struct.pack('>i', len(data)))
        self.s.sendall(data)

    def move(self, action):
        self.send({"action": "move_pixel", "payload": action})
        data = self.s.recv(2048)
        return pickle.loads(data)

    def set_pixel(self, x, y):
        self.send({"action": "set_pixel", "payload": (x, y)})
        data = self.s.recv(2048)
        return pickle.loads(data)


class Cam:
    def __init__(self, templateImg):
        self.cap = cv2.VideoCapture(0)
        self.template = cv2.imread(templateImg, 0)
        # self.template_width, self.template_height = self.template.shape[::-1]
        self.template_w, self.template_h = self.template.shape[::-1]
        self.sensitivity = 0.7

    def get_red_dot_coords(self):
        ret, img = self.cap.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img_gray, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        hits = np.where(res > self.sensitivity)
        over_threshold = False
        for x in hits:
            over_threshold = over_threshold or len(x) > 0
        if not over_threshold:
            cv2.imshow("Test", img)
            return 2000, 2000
        x = max_loc[0] + self.template_w // 2
        y = max_loc[1] + self.template_h // 2
        top_left = max_loc
        bottom_right = (top_left[0] + self.template_w, top_left[1] + self.template_h)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        cv2.imshow("Test", img)
        return x, y

    def get_center(self):
        ret, img = self.cap.read()
        h, w = img.shape[:2]
        return w//2, h//2