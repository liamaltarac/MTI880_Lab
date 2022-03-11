import gym
from gym import spaces
import numpy as np
from gym_2048.envs.demo_2048 import Demo2048

metadata = {"render_modes": ["human"]}
class Env2048(gym.Env, Demo2048):
    def __init__(self):
        super(Env2048, self).__init__()


        self.action_space = spaces.Discrete(4)

        # The observation will be the game matrix  
        self.observation_space =  spaces.Box(low=0, high=255, shape=(self.height,self.width,3), dtype=np.uint8) #spaces.Box(0, 2048, (4, 4)) #

        print('Environment initialized')

    def step(self, action): 
        state = self.shift(action)
        self.draw(None)
        self.display_score()
        
        self.reward = self.score
        if state == "won":
            self.done = True
            #self.reward = self.score
        if state == "playing":
            self.done = False
            #self.reward = 0 #self.score
        if state == "lost":
            self.done = True
            #self.reward = -1
        if state == "inv":
            self.done = False
            self.reward = -1

        observation = self.getScreenRGB()
        info = {}
        return observation, self.reward, self.done, info
        
    def reset(self):
        self.restart()
        observation = self.getScreenRGB()
        print(observation.shape)
        print('Environment reset')
        return observation

    def close(self):
        self.quit()