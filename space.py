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
        if i==0 and body2.initialized==False:
            diff = body1.position-body2.position
            length = math.sqrt(diff[0]**2+diff[1]**2)
            body1.initialized = True
            return length
        elif i==0 and body2.initialized==True:
            diff = body1.position-body2.position[i]
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

    def simulate(self):
        for i in range(0,self.steps):
            for planet in self.objects:
                if i==0:
                    planet.acs = self.acceleration(planet,i)
                else:
                    planet.acs = np.vstack((planet.acs, self.acceleration(planet,i)))
            for planet in self.objects:
                if i==0:
                    planet.velocity = np.vstack((planet.velocity,planet.velocity + planet.acs*self.stepLength))
                    planet.position = np.vstack((planet.position , planet.position + planet.velocity[i+1]*self.stepLength))
                else:
                    planet.position = np.vstack((planet.position, planet.position[i] + planet.velocity[i]*self.stepLength+(1.0/6.0)*(4*planet.acs[i]-planet.acs[i-1])*self.stepLength**2))
                    if (planet.position[i,1]==0) or (planet.position[i-1,1]<0 and planet.position[i,1]>0):
                        if planet.period == None:
                            planet.period = float(i*self.stepLength)/(60*60*24)
            if i!=0:
                for planet in self.objects:
                    tempAcs = self.acceleration(planet,i+1)
                    planet.velocity = np.vstack((planet.velocity, planet.velocity[i] + (1.0/6.0)*(2*tempAcs+5*planet.acs[i]-planet.acs[i-1])*self.stepLength))

    def init(self):
        # initialiser for animator
        return self.patches

    def animate(self, i):
        for j in range(0,len(self.objects)):
            self.patches[j].center = (self.objects[j].position[i,0], self.objects[j].position[i,1])
        return self.patches

    def run(self):
        # create plot elements
        fig = plt.figure()
        ax = plt.axes()

        # create circle of radius 0.1 centred at initial position and add to axes
        self.patches = []
        for j in range(0,len(self.objects)):
            self.patches.append(plt.Circle((self.objects[j].position[0,0], self.objects[j].position[0,1]), self.objects[j].size, color = self.objects[j].color, animated = True))
        for i in range(0,len(self.patches)):
            ax.add_patch(self.patches[i])

        # set up the axes
        ax.axis('scaled')
        ax.set_xlim(-(self.objects[2].start+10**6), self.objects[2].start+10**6)
        ax.set_ylim(-(self.objects[2].start+10**6), self.objects[2].start+10**6)
        #ax.set_xlabel('x (rads)')
        #ax.set_ylabel('sin(x)')

        # create the animator
        anim = FuncAnimation(fig, self.animate, init_func = self.init, frames = self.steps, repeat = False, interval = 1, blit = True)

        # show the plot
        plt.show()

a= Space()
a.simulate()
a.run()
print(a.objects[1].period)
