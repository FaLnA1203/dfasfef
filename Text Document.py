import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
pickle_in = open('level0_data', 'rb')
world_data = pickle.load(pickle_in)
print(world_data)