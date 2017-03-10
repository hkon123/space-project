import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class Bodies(object):

    def __init__(self,name, mass, position, size, color):
        self.name = name
        self.color = color
        self.size = size
        self.mass = mass
        self.start = position
        self.position = np.array([self.start,0])
        self.velocity = None
        self.accseleration = None
        self.period = None
