import random
import time
import cv2
from main import Socket, Cam, AgentController

s = Socket()
cam = Cam("assets/img.png")
o1 = AgentController(s.getSocket())
print("Center of image")
print(cam.get_center()[0])
print(cam.get_center()[1])
while True:
    print("Create agent controller")
    # o1 = AgentController(s.getSocket())
    """
    o1.move(Action.DOWN)
    time.sleep(0.5)
    # print(cam.detect_and_measure_distance())
    o1.move(Action.DOWN)
    time.sleep(0.5)
    o1.move(Action.DOWN)
    time.sleep(0.5)
    o1.move(Action.LEFT)
    time.sleep(0.5)
    o1.move(Action.UP)
    time.sleep(0.5)
    o1.move(Action.RIGHT)
    time.sleep(0.5)
    """
    data = o1.set_pixel(random.randint(0, 7), random.randint(0, 7))
    print("Data: ")
    print(data)
    #print(data["orientation"]["pitch"])
    # cam.detect_and_measure_distance()
    test = cam.get_red_dot_coords()
    print("Test: ")
    print(test[0])
    print(test[1])
    time.sleep(0.5)
    if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
        break

"""
while True:
    data = None
    if cv2.waitKey(10) == ord('r'):
        o1.send(s, {"action": r"set_pixel"", "payload": (random.randint(0, 7), random.randint(0, 7))})
        data = s.recv(1024)
    if cv2.waitKey(10) == ord('s'):
        o1.send(s, {"action": "move_pixel", "payload": Action.DOWN})
        data = s.recv(1024)
    if cv2.waitKey(10) == ord('w'):
        01.send(s, {"action": "move_pixel", "payload": Action.UP})
        data = s.recv(1024)
    if cv2.waitKey(10) == ord('a'):
        01.send(s, {"action": "move_pixel", "payload": Action.LEFT})
        data = s.recv(1024)
    if cv2.waitKey(10) == ord('d'):
        send(s, {"action": "move_pixel", "payload": Action.RIGHT})
        data = s.recv(1024)
    if (data is not None):
        print("Data: ", pickle.loads(data))
    detect_red_dot(cv2.imread("test2.jpg"))
    if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
        break
"""
