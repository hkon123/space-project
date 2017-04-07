import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

'''
Class to hold all the information about each body in spaceship
Takes values that determine whar kind of body it is and the bodys properties
'''


class Bodies(object):

    def __init__(self,name, mass, position, size, color, moon, ship,steps,surface):
        self.moon = moon
        self.name = name
        self.color = color
        self.size = size
        self.surface = surface
        self.mass = mass
        self.start = position
        self.ship = ship
        if self.start==0:
            self.position = np.array([self.start,0])
        elif ship == 'True':
            self.position = np.zeros((steps-1,2))
        else:
            #self.position = np.array(self.set_position())
            self.position = np.array([self.start,0])
        self.velocity = None
        if ship == 'True':
            self.velocity = np.zeros((steps,2))
        self.acs = None
        if ship == 'True':
            self.acs = np.zeros((steps-1,2))
        self.period = []
        self.initialized = False
        if ship =='True':
            self.initialized = True
        self.zeroed = None
        self.zeroPoint = np.array([0,0])
        self.zeroMark = 0
        self.orbitcount = 0
        self.orbit = False
        self.goal = None

    def set_position(self):  #Method for randomizing the planets initial position in the orbit
        xpos = random.randrange(-self.start,self.start,1)
        diff = self.start**2 -xpos**2
        if random.random()>0.5:
            ypos = math.sqrt(diff)
        else:
            ypos = -math.sqrt(diff)
        return [xpos,ypos]
