from space import Space
import time
import os
import numpy as np

'''
class to make the user decide how to use the simulation
'''

class initializing(object):

    def __init__(self):
        self.select=-1
        print("Welcome to Hakon's space-simulator")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        while self.select!=0:
            self.select=int(input("Which simulation do you want to run?\n(1):accurate simulation of solar system out to jupiter, with moons(Takes time to process)\n(2):simulation of solar system out to jupiter without moons\n(3)launch satelite from earth to mars 2 years after the start of the simulation(Takes long time to process, and some objects removed to reduce processing power needed)\n(4):add random astoroids to the solar system and see what happens(no moons)\n(5):check when the planets align\n(6):create your own solar system with your own experiments\n(0):exit program\n"))
            if self.select==1:
                a= Space(0,0,0,0,0,0,0,False,False,'everything.txt')
                a.simulate()
                a.run()
                a.plotEnergy()
                for i in range(0,len(a.objects)):
                    print(str(a.objects[i].name) +  "'s period: "),
                    print(np.mean(a.objects[i].period))
                print("\n\n")
            if self.select==2:
                a= Space(0,0,0,0,0,0,0,False,False,'nomoon.txt')
                a.simulate()
                a.run()
                a.plotEnergy()
                for i in range(0,len(a.objects)):
                    print(str(a.objects[i].name) +  "'s period: "),
                    print(np.mean(a.objects[i].period))
                print("\n\n")
            if self.select == 3:
                a= Space(1,2,0,0,'ship.txt',0,0,False,False,'launchsim.txt')
                a.simulate()
                a.run()
                a.flyBygraph(a.objects[-1],a.objects[1],a.objects[2])
                a.plotEnergy()
                print("time to reach mars:"),
                print(a.arived)
                print("Mars fly-by distance:"),
                print("%.4g" %a.flyby)
                print("\n\n")
            if self.select == 4:
                a= Space(0,0,0,0,0,0,0,True,False,'nomoon.txt')
                a.simulate()
                a.run()
                a.plotEnergy()
                for i in range(0,len(a.objects)):
                    print(str(a.objects[i].name) +  "'s period: "),
                    print(np.mean(a.objects[i].period))
                for i in range(0,len(a.crashed)):
                    print( a.crashed[i] + "crashed after " + str(float(a.crashes[i]*a.stepLength)/(60*60*24*365)) + "years")
                print("\n\n")
            if self.select == 5:
                a= Space(0,0,0,0,0,0,0,False,True,'allign.txt')
                a.simulate()
                a.plotEnergy()
                for i in a.alignements:
                    print("all planets up to mars allign after" + str(float(i*a.stepLength)/(60*60*24*365)) + "years")
                print("\n\n")
            if self.select==6:
                os.system('cls' if os.name == 'nt' else 'clear')
                universe = str(input("select universe "))
                os.system('cls' if os.name == 'nt' else 'clear')
                launches = int(input("number of satelite Launches?(max3) "))
                os.system('cls' if os.name == 'nt' else 'clear')
                start1 = int(input("startdate for 1st launch in years(if not applicaple make 0) "))
                os.system('cls' if os.name == 'nt' else 'clear')
                start2 = int(input("startdate for 2nd launch in years(if not applicaple make 0) "))
                os.system('cls' if os.name == 'nt' else 'clear')
                start3 = int(input("startdate for 3rd launch in years(if not applicaple make 0) "))
                os.system('cls' if os.name == 'nt' else 'clear')
                ship1 = str(input("shipfile for first launch? (if not aplicable make 0)"))
                os.system('cls' if os.name == 'nt' else 'clear')
                ship2 = str(input("shipfile for second launch? (if not aplicable make 0)"))
                os.system('cls' if os.name == 'nt' else 'clear')
                ship3 = str(input("shipfile for third launch? (if not aplicable make 0)"))
                os.system('cls' if os.name == 'nt' else 'clear')
                asteroid = input("add asteriods? (True/False)")
                os.system('cls' if os.name == 'nt' else 'clear')
                prob = float(input("Probability for asteroids to be added at every timestep: (f not aplicable make 0)"))
                os.system('cls' if os.name == 'nt' else 'clear')
                align = input("check for alignments?(True/False)")
                os.system('cls' if os.name == 'nt' else 'clear')
                a= Space(launches,start1,start2,start3,ship1,ship2,ship3,asteroid,align,universe)
                a.asteroidFactor = prob
                a.simulate()
                a.run()
                a.plotEnergy()
                for i in range(0,len(a.objects)):
                    print(str(a.objects[i].name) +  "'s period: "),
                    print(np.mean(a.objects[i].period))
                print("\n\n")
a = initializing()
