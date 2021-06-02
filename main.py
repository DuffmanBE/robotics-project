import random
import socket
import pickle
import struct
import cv2


def send(s, data):
    data = pickle.dumps(data)
    s.sendall(struct.pack('>i', len(data)))
    s.sendall(data)

def detect_red_dot(img):
    # ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
    ret, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    cv2.imshow("Test", img)

    #ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
    #image = cv2.resize(test_img, (640, 480))
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)q
    #cv2.imshow("Test", image)

cap = cv2.VideoCapture(0)
template = cv2.imread("assets/1a.png", 0)

template_width, template_height = template.shape[::-1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.connect(('192.168.0.218', 9395))

while True:
    send(s, {"action": "set_pixel", "payload": (random.randint(0, 7), random.randint(0, 7))})
    data = s.recv(1024)
    print("Data: ", pickle.loads(data))
    detect_red_dot(cv2.imread("img_test.jpg"))
    if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
        break



