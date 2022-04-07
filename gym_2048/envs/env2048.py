import gym
from gym import spaces
import numpy as np
from gym_2048.envs.demo_2048 import Demo2048

metadata = {"render_modes": ["human"]}
class Env2048(gym.Env, Demo2048):
    def __init__(self):
        super(Env2048, self).__init__()


        self.action_space = spaces.Discrete(4)   #spaces.Box(low=0, high=3,shape=(1,) , dtype=np.uint8 )   
        print(self.height)

        # The observation will be the game matrix  
        self.observation_space = spaces.Box(low=0, high=2048, shape=(1, 4,4)) #spaces.Box(0, 2048, (4, 4)) #
        #spaces.Box(low=0, high=2048, shape=(4,4), dtype=np.int64) #         
        print('Environment initialized')
        self.continuous_invalid_count = 0
        self.invalid_count = 0

        self.prev_score = 0
        self.steps = 0

    def step(self, action): 
        #print("Action :" , action)
        state = self.shift(action)
        self.draw(None)
        self.display_score()
        self.steps += 1
        self.reward = self.score - self.prev_score 
        #print(self.score, self.prev_score)
        
        self.prev_score = self.score
        #print("reward ",  self.reward)
        if state == "won":
            self.done = True
            #self.reward = self.score #self.score
        if state == "playing":
            self.done = False
            #self.reward = 1 #0.05
            #if self.max_tile >= 256: #Try to encourage a good strategy. if we made it this far, it's probably doing something right.
            
            #if self.score > 0:
                #self.reward =  int(np.log(self.score + 1)) # / 2048
            self.continuous_invalid_count = 0

            #self.reward = self.score/2048
        if state == "lost":
            self.done = True
            #self.reward = -10

            #self.reward+= 0 #self.invalid_cont
            #print("inv")
        if state == "inv":
            self.done = False
            self.invalid_count += 1 
            self.continuous_invalid_count += 1
            if self.continuous_invalid_count >= 10 :
                #self.done = True
                self.reward = self.continuous_invalid_count * -100



        observation = self.get_board() #self.getScreenRGB()
        #print(observation)
        info = {}
        return observation, self.reward, self.done, info
        
    def reset(self):
        self.restart()
        self.prev_score = 0
        self.invalid_count = 0
        self.continuous_invalid_count = 0
        self.steps = 0

        observation = self.get_board() # self.getScreenRGB()
        #self.invalid_cont = 0
        print('Environment reset')
        return observation

    def close(self):
        self.quit()