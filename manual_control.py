#!/usr/bin/env python3

import time
import argparse
import numpy as np
import gym
import gym_2048
from pygame.locals import *
import pygame


def reset():
    obs = env.reset()

def step(action):
    obs, reward, done, info = env.step(action)
    print('reward=%.9f' % (reward))

    if done:
        print('done!')
        reset()

def run():

    while 1: 
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                env.close()
                return

            if key_pressed[pygame.K_LEFT]:
                step(0)

            if key_pressed[pygame.K_RIGHT]:
                step(1)

            if key_pressed[pygame.K_UP]:
                step(2)
                

            if key_pressed[pygame.K_DOWN]:
                step(3)


env = gym.make('Env2048-v1')
reset()

run()





