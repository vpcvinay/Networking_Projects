
# coding: utf-8

# In[20]:


# Name:  Vemali. Purna Chandra Vinay Kumar
# net Id: pxv171630@utdallas.edu

import numpy as np
import exponential as rand_expo
import pylab as py

# class for generating and sorting the arrivals 
# from the L terminals
# creates a list of arrivals and sorts according 
# to the arrival time in descending chronoogical order


class generate_arri:
    
    def __init__(self,L=0):
        
        # dict of the terminal containg the terminal number 
        # and the arraival time and count used to represent
        # if the arrived process is serviced or not
        
        self.terminal = {'count':0,'time':0,'num':0,'ty':'arrival'}
        self.ter_list = []
        self.L        = L
        self.lam      = 0.3
    
    # sorts the list of terminal arrivals in chonological order
    # of arrival time
       
    def sorting(self,ter_list):
        event = 'time'
        j = 0
        for ter in self.ter_list:
            arr_j = ter.__getitem__(event)
            k = 0
            for ter_2 in self.ter_list:
                update = False
                arr_k = ter_2.__getitem__(event)
                if(arr_j<arr_k and k>j):
                    temp = ter_list[k]
                    update = True
                    
                if(update==True):
                    ter_list[k] = ter_list[j]
                    ter_list[j] = temp
                    
                k += 1
            j += 1
                    
        return ter_list
    
    # generates the arrival time from the terminal i
    
    def gen_arr(self,i):
        self.terminal.__setitem__('num',i)
        arr_time = rand_expo.expo_rand(self.lam)
        self.terminal.__setitem__('time',arr_time)
        self.terminal.__setitem__('count',1)
        self.ter_list.append(self.terminal.copy())
        sorted_list = self.sorting(self.ter_list)
        self.ter_list = sorted_list
    
    # creats the list of terminal arrivals
        
    def create_list(self):
        for i in range(self.L):
            self.gen_arr(i)
            
# dict of the customer being serviced containing the departure 
# time and the terminal from which the customer arrived

class system_state(generate_arri):
    def __init__(self,L=10,K=4,M=2,mu=3):
        
        self.server      = {'time':0,'num':0,'ty':'depart'}
        self.queue       = []
        self.clock       = 0
        self.prev = 0
        self.event_count = 0
        self.EN          = 0
        self.Ndep        = 0
        self.n           = 100000
        self.L           = L
        self.M           = M
        self.K           = K
        self.p           = p
        self.mu          = mu
        generate_arri.__init__(self,L=self.L)
    
    # creates the list of terminal arivals
    
    def list_creating(self):
        self.create_list()
            
    # function of the arrival event
    
    def arrival_event(self):
        self.prev = self.clock
        self.queue.append(self.ter_list.pop())
        self.event_count += 1
        arr_time = self.queue[len(self.queue)-1].__getitem__('time')
        self.clock = self.clock+arr_time
        self.EN += self.event_count*arr_time
    
    # updates the system
    
    def queue_process(self):
        self.arrival_event()
        while(self.Ndep<=self.n):
            while(self.event_count<=self.K and self.Ndep<=self.n):
                while(self.event_count<=self.M and self.Ndep<=self.n):
                    ty = self.queue[len(self.queue)-1].__getitem__('ty')
                    if(ty=='arrival'):
                        ser_time = rand_expo.expo_rand(self.mu)
                        self.prev = self.clock
                        dep_time = self.clock+ser_time
                        temp = self.queue.pop()
                        ID = temp.__getitem__('num')
                        
                        self.server.__setitem__('time',dep_time)
                        self.server.__setitem__('num',ID)
                        self.queue.append(self.server.copy())
                        self.queue = self.sorting(self.queue)
                        
                    elif(ty=='depart'):
                        self.event_count -= 1
                        temp = self.queue.pop()
                        time = temp.__getitem__('time')
                        
                        ID = temp.__getitem__('num')
                        self.gen_arr(ID)
                        self.Ndep += 1
                        
                    arr_time = self.ter_list[len(self.ter_list)-1].__getitem__('time')
                    self.queue.append(self.ter_list.pop())
                    self.event_count += 1
                    self.queue = self.sorting(self.queue)
                    self.clock = self.clock+arr_time
                    self.EN += self.event_count*arr_time
                
                        
                if(ty=='depart'):
                    self.event_count -= 1
                    temp = self.queue.pop()
                    time = temp.__getitem__('time')
                    
                    ID = temp.__getitem__('num')
                    self.gen_arr(ID)
                    self.Ndep += 1
                
                else:
                    arr_time = self.ter_list[len(self.ter_list)-1].__getitem__('time')
                    self.queue.append(self.ter_list.pop())
                    self.event_count += 1
                    self.queue = self.sorting(self.queue)
                    self.clock = self.clock+arr_time
                    self.EN += self.event_count*arr_time
                    
            
            for j in range(len(self.queue)):
                ty = self.queue[j].__getitem__('ty')
                if(ty=='depart'):
                    self.event_count -= 1
                    temp = self.queue.pop(j)
                    time = temp.__getitem__('time')
                    self.clock = time
                    ID = temp.__getitem__('num')
                    self.gen_arr(ID)
                    self.Ndep += 1
                    break
                    

# inputs for the system 

L = int(input("enter the number of terminals L"))
M = int(input("enter the number of servers M"))
K = int(input("enter the size of the queue including the server size K"))
mu = int(input("enter the service rate mu"))
p = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    
event_count = []
EN = []

#calculates the epection and state for the value of p = 0.1-1.0
for t in p:
    sys = system_state(L=L,M=M,K=K,mu=mu)
    lam = t*M*mu
    sys.lam = lam
    sys.list_creating()
    sys.queue_process()
    event_count.append(sys.event_count)
    EN.append(sys.EN/sys.clock)

lam = np.array(p)*M*mu

print("The expected number of customers of the p = 0.1-1.0",EN)
print("The state of the system for the p = 0.1-1.0",event_count)

py.plot(lam,EN)
py.legend(['sim'])
py.xlabel('lambda')
py.ylabel('Expectation')
py.show()


# In[ ]:




