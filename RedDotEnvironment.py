import gym
import numpy as np
from gym import spaces
from enum import Enum

from main import Socket, AgentController, Cam


class Action(Enum):
    NOTHING = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class RedDotEnvironment(gym.Env):
    """Custom environment that follows gym interface"""

    def __init__(self):
        super().__init__()
        self.s = Socket()
        self.agentController = AgentController(self.s.getSocket())
        self.cam = Cam("assets/img.png")
        self.center_of_image = self.cam.get_center()
        self.current_step = 0

        # The environment implements 4 actions: move the red dot up/down/left/right in the LED matrix of the Raspberry Pi.
        # I figured the agent can also decide to do nothing which is a fifth action.
        self.action_space = gym.spaces.Discrete(5)

        # 8 values:
        # orientation: pitch, roll, yaw
        # accelerometer: x, y, z
        # x, y location of red dot in the image observed by the webcam.
        self.observation_space = spaces.Box(low=0, high=1, shape=(8,), dtype=np.float16)

    def reset(self):
        print("Reset!")
        self.current_step = 0
        self.agentController = AgentController(self.s.getSocket())
        return np.array([
            0, 0, 0, 0, 0, 0, 0, 0
        ])

    def step(self, action):
        # Execute one time step within the environment
        sensehat_props = self._take_action(action)
        orientation = sensehat_props["orientation"]
        accelerometer = sensehat_props["accelerometer"]
        self.current_step = self.current_step + 1
        red_dot_position = self.cam.get_red_dot_coords()

        #reward: center x - red_dot_x + center y - red dot y
        # reward = self.center_of_image[0] - red_dot_position[0] + self.center_of_image[1] - red_dot_position[1]
        reward = self.center_of_image[0] - abs(self.center_of_image[0] - red_dot_position[0]) + \
                 self.center_of_image[1] - abs(self.center_of_image[1] - red_dot_position[1])
        print("Reward: ")
        print(reward)
        obs =  np.array([
            orientation["pitch"],
            orientation["roll"],
            orientation["yaw"],
            accelerometer["x"],
            accelerometer["y"],
            accelerometer["z"],
            red_dot_position[0],
            red_dot_position[1]
        ])

        done = self.current_step == 100 or reward > 900
        print("Done: ")
        print(done)
        return obs, reward, done, {}
    """
    returns object in this format:
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
	"""
    def _take_action(self, action):
        data = self.agentController.move(action)
        return data
