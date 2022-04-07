import gym
import torch as th
import torch.nn as nn
from stable_baselines3.dqn.policies import DQNPolicy

from stable_baselines3 import PPO
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class CustomCNN(BaseFeaturesExtractor):
    """
    :param observation_space: (gym.Space)
    :param features_dim: (int) Number of features extracted.
        This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 4):
        super(CustomCNN, self).__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        n_input_channels = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32, kernel_size=2, stride=1, padding=0),   #128@3x3
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=2, stride=1, padding=0), #128@2x2
            nn.ReLU(),
            nn.Flatten(),
            #nn.Linear(512, 256),
            #nn.Linear(256, 4)
        )

        # Compute shape by doing one forward pass
        '''with th.no_grad():
            n_flatten = self.cnn(
                th.as_tensor(observation_space.sample()[None]).float()
            ).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())'''

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.cnn(observations) #self.linear()

