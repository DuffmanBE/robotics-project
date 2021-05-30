import socket
import pickle
import struct
from sense_hat import SenseHat


def recv(s):
	data = s.recv(4, socket.MSG_WAITALL)
	data_len = struct.unpack('>i', data)[0]
	data = pickle.loads(s.recv(data_len, socket.MSG_WAITALL))
	print("Received data!", data)
	if 'action' in data:
		if data["action"] == "set_pixel":
			coordinates = data["payload"]
			sense.clear()
			sense.set_pixel(coordinates[0], coordinates[1], 255, 0, 0)
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


