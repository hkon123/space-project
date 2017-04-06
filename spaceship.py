import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

class SpaceShip(object):

    def __init__(self, name, mass, start):
        self.name = name
        self.mass = mass
        self.position = None
        self.start = start
        self.velocity = None
        self.acs = None
