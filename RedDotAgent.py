import gym
from stable_baselines3 import PPO
import RedDotEnvironment as environment

env = environment.RedDotEnvironment()

agent = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./logs/progress/", n_steps=128)
agent.learn(total_timesteps= 5000)
agent.save("./agents/ppo_firstTry")