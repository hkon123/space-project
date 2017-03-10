import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from bodies import Bodies


class Space(object):

    def __init__(self):
        self.G = 6.67408*10**-11
        self.objects=[]
        self.info =[]
        self.names = []
        self.masses = []
        self.positions = []
        self.sizes = []
        self.colors = []
        with open('info.txt','r') as f:
            for line in f:
                for word in line.split():
                    self.info.append(word)
        k=0
        while self.info[k]!= 'end':
            if self.info[k] == 'new':
                self.names.append(self.info[k+1])
                self.masses.append(float(self.info[k+3]))
                self.positions.append(float(self.info[k+5]))
                self.sizes.append(float(self.info[k+7]))
                self.colors.append(self.info[k+9])
            if self.info[k] == 'details':
                self.stepLength = int(self.info[k+2])
                self.steps = int(self.info[k+4])
            k+=1
        for i in range(0,len(self.names)):
            self.objects.append(Bodies(self.names[i],self.masses[i],self.positions[i],self.sizes[i],self.colors[i]))
        for i in self.objects:
            speed = 0
            for j in self.objects:
                if i==j:
                    continue
                else:
                    speed += math.sqrt(self.G*j.mass/math.sqrt((i.start-j.start)**2))
            i.velocity = np.array([0,speed])


    def distance(self,body1,body2,i):
        if i==0:
            diff = body1.position-body2.position
            length = math.sqrt(diff[0]**2+diff[1]**2)
            return length
        else:
            diff = body1.position[i]-body2.position[i]
            length = math.sqrt(diff[0]**2+diff[1]**2)
            return length

    def direction(self, body1, body2, i):
        if i==0:
            direct = (body1.position-body2.position)/self.distance(body1,body2,i)
            return direct
        else:
            direct = (body1.position[i]-body2.position[i])/self.distance(body1,body2,i)
            return direct

    def acceleration(self,body,i):
        accs = np.array([0,0])
        for j in self.objects:
            if body==j:
                continue
            else:
                accs = accs + self.direction(body, j, i)*(-self.G)*(j.mass/(self.distance(body, j, i))**2)
        return accs
