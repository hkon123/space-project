import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random



class Bodies(object):

    def __init__(self,name, mass, position, size, color, moon):
        self.moon = moon
        self.name = name
        self.color = color
        self.size = size
        self.mass = mass
        self.start = position
        if self.start==0:
            self.position = np.array([self.start,0])
        else:
            self.position = np.array(self.set_position())
        self.velocity = None
        self.acs = None
        self.period = []
        self.initialized = False
        self.zeroed = None

    def set_position(self):
        xpos = random.randrange(-self.start,self.start,1)
        diff = self.start**2 -xpos**2
        ypos = math.sqrt(diff)
        return [xpos,ypos]
