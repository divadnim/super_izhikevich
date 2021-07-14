#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:49:10 2021

@author: davidsm
Izhikevich Cell Super Class and Subclasses
"""
import numpy as np
import matplotlib.pyplot as plt

class izhCell():
    def __init__(self, stimVal):
        #Define equation parameters
        self.celltype = "Regular Spiking"
        self.a = 0.03
        self.b = -2
        self.c = -50
        self.d = 100
        self.vpeak = 35
        self.k = .7
        #self.f =
        self.C = 100
        self.vt = -40 #threshold voltage
        self.vr = -60 #reset voltage
        self.stimVal = stimVal #level of current supplied to cell input
        
        self.T = 1000 #ms
        self.tau = 1 #ms -- time step
        self.n = int(np.round(self.T/self.tau))
        
        #Stimulation
        self.I = np.concatenate((np.zeros((1,int(self.n*0.1))),self.stimVal*np.ones((1,int(self.n*0.9)))),axis=1)
        
        #Results Placeholder
        self.v = self.vr * np.ones((1, self.n))
        self.u = 0 * self.v
    """this code is supposed to create the parameters of the graph in order to run the 
    be able to recreate the plot using python
    the super allows me to access the functions and methods created in the 
    original regular spiking part of the code and use it in the 
    intrinsic bursting and the chattering part of the code
    with respective changes to the parameters
    """
        
    def __repr__(self):
        return self.celltype + "Cell w Input Current =" + str(self.stimVal)
    
    def simulate(self):
        for i in range(0, self.n-1):
            #self.v[0,i+1] = self.v[0,i] + self.tau*(self.k*(self.v[0,i] - self.vr))*((self.v[0,i] - self.vt) - self.u[0,i] + self.I[0,i])/self.C
            self.v[0,i+1] = self.v[0,i] + self.tau*(self.k*(self.v[0,i]-self.vr) * (self.v[0,i] - self.vt) - self.u[0,i] + self.I[0,i])/self.C

            #self.u[0,i+1]= self.u[0,i] + self.tau*self.a*(self.b*(self.v[0,i]-self.vr) - self.u[0,i])
            self.u[0,i+1] = self.u[0,i] + self.tau*self.a*(self.b*(self.v[0,i] - self.vr) - self.u[0,i])

            if self.v[0,i+1] >= self.vpeak:
                self.v[0,i] = self.vpeak
                self.v[0,i+1] = self.c
                self.u[0,i+1] = self.u[0, i+1] + self.d
                
def plot_my_data(somecell, upLim = 1000):
    tau = somecell.tau
    n = somecell.n
    v = somecell.v
    celltype = somecell.celltype
    
    fig = plt.figure()
    plt.plot(tau*np.arange(0,n), v[0,:].transpose(), "k-")
    plt.xlabel("Time Step")
    plt.xlim([0, upLim])
    plt.ylabel(celltype + "Cell Response")
    
    
                
mycell = izhCell(100)
mycell.simulate()
plot_my_data(mycell)

class intrinsicBursting(izhCell):
    def __init__(self, stimVal):
        super().__init__(stimVal)
        self.celltype = "Intrinsic Bursting"
        self.a = 0.01
        self.b = 5
        self.c = -56
        self.d = 150
        self.vpeak = 50
        self.k = 1.2
        #self.f =
        self.C = 130
        self.vt = -45 #threshold voltage
        self.vr = -75 #reset voltage
        self.stimVal = stimVal #level of current supplied to cell input
        
        self.T = 1000 #ms
        self.tau = 1 #ms -- time step
        self.n = int(np.round(self.T/self.tau))
        
        
    def __repr__(self):
        return self.celltype + "Cell w Input Current =" + str(self.stimVal)
    
    def simulate(self):
        super().simulate()
        
    def plot_my_data(self, somecell):
        super().plot_my_data(self, somecell, upLim = 1000)
        
testcell = intrinsicBursting(200)
testcell.simulate()
plot_my_data(testcell)

class Chattering(izhCell):
    def __init__(self, stimVal):
        super().__init__(stimVal) 
        self.celltype = "Chattering"
        self.a = 0.03
        self.b = 1
        self.c = -40
        self.d = 50
        self.vpeak = 25
        self.k = 1.5
        #self.f =
        self.C = 150
        self.vt = -40 #threshold voltage
        self.vr = -60 #reset voltage
        self.stimVal = stimVal #level of current supplied to cell input
        
        self.T = 1000 #ms
        self.tau = 1 #ms -- time step
        self.n = int(np.round(self.T/self.tau))
        
        
    def __repr__(self):
        return self.celltype + "Cell w Input Current =" + str(self.stimVal)
    
    def simulate(self):
        super().simulate()
        
    def plot_my_data(self, somecell):
        super().plot_my_data(self, somecell, upLim = 1000)
        
testcell2 = Chattering(100)
testcell2.simulate()
plot_my_data(testcell2)