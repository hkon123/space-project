import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random



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
        self.goal = 'mars'

    def set_position(self):
        xpos = random.randrange(-self.start,self.start,1)
        diff = self.start**2 -xpos**2
        ypos = math.sqrt(diff)
        return [xpos,ypos]
