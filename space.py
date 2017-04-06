import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from bodies import Bodies
from spaceship import SpaceShip
import os
import random

class Space(object):

    def __init__(self):
        self.G = 6.67408*10**-11
        self.objects=[]
        self.ships = []
        self.info =[]
        self.names = []
        self.masses = []
        self.positions = []
        self.sizes = []
        self.colors = []
        self.moons = []
        self.count = 2
        self.reset = None
        self.switch = None
        self.arived = None
        self.flyby = None
        self.ships = []
        self.surfaces = []
        self.alignements = []
        self.alignement = None



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
                self.moons.append(self.info[k+11])
                self.ships.append(self.info[k+13])
                self.surfaces.append(float(self.info[k+15]))
            if self.info[k] == 'details':
                self.stepLength = int(self.info[k+2])
                self.steps = int(self.info[k+4])
            k+=1
        for i in range(0,len(self.names)):
            self.objects.append(Bodies(self.names[i],self.masses[i],self.positions[i],self.sizes[i],self.colors[i],self.moons[i],self.ships[i],0,self.surfaces[i]))
            if self.objects[i].moon !="no":
                for j in self.objects:
                    if self.objects[i].moon == j.name:
                        planetLength = self.distance(j,self.objects[0],0,False)
                        planetDirection = self.direction(j,self.objects[0],0)
                        self.objects[i].position = planetDirection*self.objects[i].start + planetDirection*planetLength
                        print(self.distance(j,self.objects[i],0,False))

        for i in self.objects:
            #speed = np.array([0,0])
            i.velocity = np.array([0,0])
            if i == self.objects[0]:
                self.zeroPoint=np.array([0,0])
                continue
            else:
                i.velocity = i.velocity + math.sqrt(self.G*self.objects[0].mass/self.distance(i,self.objects[0],0,False))*self.normalize(self.direction(i,self.objects[0],0))
            if i.moon!="no":
                for j in self.objects:
                    if i==j or i.moon!=j.name:
                        continue
                    else:
                        i.velocity = i.velocity + math.sqrt(self.G*j.mass/self.distance(j,i,0,False))*self.normalize(self.direction(i,j,0))
                    #speed += math.sqrt(self.G*j.mass/math.sqrt((i.start-j.start)**2))
            #i.velocity = np.array([0,speed])
            #i.velocity = speed
            i.zeroPoint = self.absDirection(i.velocity,0,0)
            print(i.zeroPoint[0])
        self.launch = self.steps

    def absDirection(self, vector,i,element):
        if i==0:
            direct = vector/math.sqrt(vector[0]**2+vector[1]**2)
            if element==0:
                return direct
            elif element==1:
                return direct[0]
            elif element == 2:
                return direct[1]
        else:
            tempVector= vector[i]
            direct = tempVector/math.sqrt(tempVector[0]**2+tempVector[1]**2)
            if element==0:
                return direct
            elif element==1:
                return direct[0]
            elif element == 2:
                return direct[1]

    def absLength(self,vector,i):
        if i == False:
            length = math.sqrt(vector[0]**2+vector[1]**2)
            return length
        else:
            tempVector = vector[i]
            length = math.sqrt(tempVector[0]**2+tempVector[1]**2)
            return length

    def energy(self,i):
        tot = 0
        for k in self.objects:
            tot+= 0.5*k.mass*self.absLength(k.velocity,i)**2
        return tot



    def normalize(self, vector):
        e1 = -1*vector[1]
        e2 = vector[0]
        newVector = np.array([e1,e2])
        return newVector

    def distance(self,body1,body2,i, sett):
        if i==0 and body2.initialized==False:
            diff = body1.position-body2.position
            length = math.sqrt(diff[0]**2+diff[1]**2)
            if sett == True:
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
            direct = (body1.position-body2.position)/self.distance(body1,body2,i,False)
            return direct
        else:
            direct = (body1.position[i]-body2.position[i])/self.distance(body1,body2,i,False)
            return direct

    def rotateVector(self, vector, degrees):
        x = vector[0]*math.cos(degrees) + vector[1]*math.sin(degrees)
        y = vector[1]*math.cos(degrees) - vector[0]*math.sin(degrees)
        return np.array([x,y])


    def addRandomCelestial(self,i):
        mass = random.randrange(10**10,10**17)
        size = 1000000000
        color = 'k'
        self.objects.append(Bodies('asteroid', mass, 1, size, color, 'no', 'True', i, 100000))
        xpos = random.randrange(-1e14,1e14)
        ypos = random.randrange(-1e14,1e14)
        self.objects[-1].position = np.vstack((self.objects[-1].position, np.array([xpos,ypos])))
        self.objects[-1].position = np.vstack((self.objects[-1].position, np.array([xpos,ypos])))
        xvel = random.randrange(-15000,15000)
        yvel = random.randrange(-15000,15000)
        self.objects[-1].velocity = np.vstack((self.objects[-1].velocity, np.array([xvel,yvel])))
        self.objects[-1].acs = np.vstack((self.objects[-1].acs, self.acceleration(self.objects[-1],i-1)))


    def shipAcsOrbit(self,ship,acs,i, rotate, deg):
        for j in self.objects:
            if ship.goal == j.name:
                #if ship.orbit == False:
                    #for k in xrange(int(self.distance(ship, j, i-1, False)),int(self.distance(ship, j, i, False))):
                        #if k%int(((float(3e8))/90))==0:
                            #print("hei")
                            #ship.orbitcount+=1
                            #if ship.orbitcount == 90:
                                #ship.orbit = True
                                #print("hei2")
                acsDirection = self.direction(j,ship,i)
                if rotate == True:
                    acsDirection = self.rotateVector(acsDirection,math.radians(deg))
                accs = acsDirection*acs
                return accs

    def setShipVel(self,ship,i,vel,rotate,deg):
        for j in self.objects:
            if ship.goal == j.name:
                velDirection = self.direction(j,ship,i)
                if rotate == True:
                    velDirection = self.rotateVector(velDirection,math.radians(deg))
                velo = velDirection*vel
                return velo

    def relativeVelocity(self,body1,body2,i):
        diff = body2.velocity[i]-body1.velocity[i]
        return self.absLength(diff,False)


    def acceleration(self,body,i):
        accs = np.array([0,0])
        for j in self.objects:
            if body==j:
                continue
            else:
                accs = accs + self.direction(body, j, i)*(-self.G)*(j.mass/(self.distance(body, j, i,True))**2)
                if i>10:
                    if self.distance(body, j, i,False)<=j.surface:
                        #accs = accs - self.direction(body, j, i)*(-self.G)*(j.mass/(self.distance(body, j, i,True))**2)
                        print("CRASH!!!"),
                        print(self.distance(body, j, i,False))
                        print(j.surface)
                        print(body.name),
                        print(j.name)
        #if body.ship == 'True' and i>4:
        #    if self.distance(body,self.objects[1],i-1,False)<10000+6371000:
        #        accs = accs + self.shipAcsOrbit(body,3, i,True, -10)
        #    elif self.distance(body,self.objects[4],i-1,False)>23.463e7:
        #        accs = accs + self.shipAcsOrbit(body,0.001, i,True,-5)
        #    else:
        #        accs = accs + self.shipAcsOrbit(body,0.001, i,False,0)
        return accs

    def getShip(self,i,shipfile,deltaV,angle):
        with open(shipfile,'r') as f:
            for line in f:
                for word in line.split():
                    self.ships.append(word)

        k=0
        while self.ships[k]!= 'end':
            if self.ships[k] == 'new':
                self.names.append(self.ships[k+1])
                self.masses.append(float(self.ships[k+3]))
                self.positions.append(float(self.ships[k+5]))
                self.sizes.append(float(self.ships[k+7]))
                self.colors.append(self.ships[k+9])
                self.moons.append(self.ships[k+11])
                self.ships.append(self.ships[k+13])
                self.surfaces.append(float(self.ships[k+15]))
            k+=1
        self.objects.append(Bodies(self.names[-1],self.masses[-1],self.positions[-1],self.sizes[-1],self.colors[-1],self.moons[-1],self.ships[-1],i,self.surfaces[-1]))
        for j in self.objects:
            if self.objects[-1].moon == j.name:
                previousLenght = self.distance(j,self.objects[0],i-1,False)
                previousDirection = self.direction(j,self.objects[0],i-1)
                planetLength = self.distance(j,self.objects[0],i,False)
                planetDirection = self.direction(j,self.objects[0],i)
                self.objects[-1].position = np.vstack((self.objects[-1].position,previousDirection*self.objects[-1].start + previousDirection*previousLenght))
                self.objects[-1].position = np.vstack((self.objects[-1].position,planetDirection*self.objects[-1].start + planetDirection*planetLength))
                planetTan = self.normalize(self.direction(self.objects[-1],j,i))
        sunVel = math.sqrt(self.G*self.objects[0].mass/self.distance(self.objects[-1],self.objects[0],i,False))*self.normalize(self.direction(self.objects[-1],self.objects[0],i))
        planetVel = planetTan*460
        launchVel = self.setShipVel(self.objects[-1],i,deltaV,True,angle)
        #launchVel = planetTan*deltaV
        #launchVel = self.normalize(self.direction(self.objects[0],self.objects[-1],i))
        self.objects[-1].velocity = np.vstack((self.objects[-1].velocity, sunVel + planetVel + launchVel))
        #self.objects[-1].velocity = self.objects[-1].velocity + self.setShipVel(self.objects[-1],i,5000,True,-10)
        self.objects[-1].acs = np.vstack((self.objects[-1].acs, self.acceleration(self.objects[-1],i-1)))
        print(self.objects[1].acs[i-1])
        print(self.objects[-1].acs[i-1])
        print(self.acceleration(self.objects[-1],i))
        print(self.objects[-1].position[i-1])
        print(self.objects[1].position[i-1])
        print(self.objects[-1].position[i])
        print(self.objects[1].position[i])

    def simulate(self):
        progress=1
        for i in range(0,self.steps):
            if i%(self.steps/100)==0:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("progress: " + str(progress) + "%")
                progress+=1
                #if progress == 7:
                #    self.stepLength= self.stepLength*50
                #    self.switch = i
            if i== int(float(365*2*(60*60*24))/self.stepLength):
                #self.getShip(i,'ship.txt',10000,44.339)
                self.launch = i
            #if random.random()<0.00005:
            #    self.addRandomCelestial(i)
            #    print("add")
            for planet in self.objects:
                if i==0:
                    planet.acs = self.acceleration(planet,i)
                else:
                    planet.acs = np.vstack((planet.acs, self.acceleration(planet,i)))
            for planet in self.objects:
                if i==0:
                    planet.velocity = np.vstack((planet.velocity, planet.velocity + planet.acs*self.stepLength))
                    planet.position = np.vstack((planet.position , planet.position + planet.velocity[i+1]*self.stepLength))
                else:
                    #planet.velocity = np.vstack((planet.velocity, planet.velocity[i] + planet.acs[i]*self.stepLength))
                    #planet.position = np.vstack((planet.position , planet.position[i] + planet.velocity[i+1]*self.stepLength))
                    planet.position = np.vstack((planet.position, planet.position[i] + planet.velocity[i]*self.stepLength+(1.0/6.0)*(4*planet.acs[i]-planet.acs[i-1])*self.stepLength**2))
                    if (planet.position[i,1]==0) or (planet.position[i-1,1]<0 and planet.position[i,1]>0):
                        if planet.zeroed == None:
                            planet.zeroed = i
                        else:
                            planet.period.append(float((i-planet.zeroed)*self.stepLength)/(60*60*24))
                            planet.zeroed = i
                    if  i>2525 :
                        if self.absDirection(planet.velocity,i-1,1)<planet.zeroPoint[0] and self.absDirection(planet.velocity,i-1,2)>planet.zeroPoint[1] and self.absDirection(planet.velocity,i,1)>planet.zeroPoint[0] and self.absDirection(planet.velocity,i,2)<planet.zeroPoint[1]:
                            planet.period.append(float((i-planet.zeroMark)*self.stepLength)/(60*60*24))
                            planet.zeroMark = i
                    if planet.ship=='True':
                        #if self.distance(self.objects[3], self.objects[1], i-1, False)<10000+6371000 and self.distance(self.objects[3], self.objects[1], i, False)>10000+6371000:
                        #    self.escape = float((i)*self.stepLength)/(60*60*24)
                        if self.distance(planet, self.objects[2], i-1, False)<self.distance(self.objects[2], planet, i, False) and self.arived==None and i>self.launch+1000:
                            self.arived = float((i-self.launch)*self.stepLength)/(60*60*24)
                                          #float((i-self.launch)*self.stepLength)/(60*60*24)
                            self.flyby = self.distance(planet, self.objects[2], i-1, False)
                    #if (planet.position[i-2,0]<planet.position[i-1,0] and planet.position[i-1,0]>planet.position[i,0] and i>10):
                    #    planet.period.append(float((i-1)*self.stepLength)/(60*60*24))
            if i!=0:
                self.checkAlignment(i)
                for planet in self.objects:
                    tempAcs = self.acceleration(planet,i+1)
                    planet.velocity = np.vstack((planet.velocity, planet.velocity[i] + (1.0/6.0)*(2*tempAcs+5*planet.acs[i]-planet.acs[i-1])*self.stepLength))


    def init(self):
        # initialiser for animator
        return self.patches

    def animate(self, i):
        if i >2:
            #if i%(self.steps/100)==0:
            #    self.count+=1
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Total kinetic energy of the system: "),
            print(self.energy(i)),
            print("joules")
            print("days into the simulation: "),
            #if self.count<7:
            print(float((i)*self.stepLength)/(60*60*24))
        if i>self.launch:
            print("days after launch: "),
            print(float((i-self.launch)*self.stepLength)/(60*60*24))
            #if self.count == 7 and self.reset==None:
            #    self.reset = float((i)*self.stepLength)-float((i)*float(self.stepLength)/50)
            #if self.count>=7:
            #    print(float((i)*self.stepLength-self.reset)/(60*60*24))
        #if i>4:
            #print(self.distance(self.objects[3], self.objects[4], i, False))
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
        ax.set_xlim(-10**12, 10**12)
        ax.set_ylim(-10**12, 10**12)
        #ax.set_xlabel('x (rads)')
        #ax.set_ylabel('sin(x)')

        # create the animator
        anim = FuncAnimation(fig, self.animate, init_func = self.init, frames = self.steps, repeat = False, interval = 0.1, blit = True)
        # show the plot
        plt.show()



    def flyBygraph(self,probe,start,goal):
        startDistances = []
        goalDistances = []
        time = 0
        times = []
        for i in xrange(int(float(365*2*(60*60*24))/self.stepLength),self.steps):
            startDistances.append(self.distance(start, probe, i, False))
            goalDistances.append(self.distance(goal, probe, i, False))
            times.append(time)
            time = time + float(self.stepLength)/(60*60*24)

        #plt.plot(times, startDistances, 'r')
        plt.plot(times, goalDistances,'b', times , startDistances, 'r')
        plt.xlabel('time in days after launch')
        plt.ylabel('Distance from planets(blue:start red:goal)')
        plt.title('probes distances')
        plt.show()

    def plotEnergy(self):
        totEnergy = []
        times = []
        time = 0
        for i in xrange(1,self.steps):
            totEnergy.append(self.energy(i))
            times.append(time)
            time = time + float(self.stepLength)/(60*60*24)

        plt.plot(times,totEnergy)
        plt.xlabel('time in days')
        plt.ylabel('total kinetic energy')
        plt.title('plot of total kinetic energy')
        plt.show()

    def checkAlignment(self,i):
        alignementVector = self.direction(self.objects[2],self.objects[0],i)
        tot = 0
        aligned = 0
        for planet in self.objects:
            if planet.moon == 'no' and planet.ship == 'False' and planet.name!= 'sun':
                tot+=1
                divAngle = math.atan(float(planet.surface+10000000000)/self.distance(planet,self.objects[0],i, False))
                posdirection = self.rotateVector(alignementVector, -divAngle)
                negdirection = self.rotateVector(alignementVector, divAngle)
                planetdirection = self.direction(planet,self.objects[0],i)
                if alignementVector[0]>0 and alignementVector[1]>0:
                    if (planetdirection[0]>posdirection[0] and planetdirection[0]<negdirection[0]):
                        if (planetdirection[1]>negdirection[1] and planetdirection[1]<posdirection[1]):
                            aligned +=1
                if alignementVector[0]<0 and alignementVector[1]>0:
                    if (planetdirection[0]>posdirection[0] and planetdirection[0]<negdirection[0]):
                        if (planetdirection[1]<negdirection[1] and planetdirection[1]>posdirection[1]):
                            aligned +=1
                if alignementVector[0]<0 and alignementVector[1]<0:
                    if (planetdirection[0]<posdirection[0] and planetdirection[0]>negdirection[0]):
                        if (planetdirection[1]<negdirection[1] and planetdirection[1]>posdirection[1]):
                            aligned +=1
                if alignementVector[0]>0 and alignementVector[1]<0:
                    if (planetdirection[0]<posdirection[0] and planetdirection[0]>negdirection[0]):
                        if (planetdirection[1]>negdirection[1] and planetdirection[1]<posdirection[1]):
                            aligned +=1
        if tot == aligned:
            self.alignements.append(i)
            self.alignement = i
            print("we have an alignement at" + str(float(i*self.stepLength)/(60*60*24*365))+ "years")

a= Space()
a.simulate()
#a.run()
#a.flyBygraph(a.objects[-1],a.objects[1],a.objects[2])
a.plotEnergy()
for i in range(0,len(a.objects)):
    print(str(a.objects[i].name) +  "'s period: "),
    print(a.objects[i].period)

#print("time to escape earth:"),
#print(a.escape)
#print("time to reach mars:"),
#print(a.arived)
#print("Mars fly-by distance:"),
#print("%.4g" %a.flyby)
