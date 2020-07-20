#   --------- Network Reliability Problem ----------- #

import numpy as np
import matplotlib.pyplot as plt

#%matplotlib

# Create a list, which stores the Link condition 'up' or 'down'
# Initially set the all the links state to 'down'
# list contains series of '1' (defines 'up' state) and '0' (defines 'down' state)
# Number of links n = 10

# Link[i+j] defines the link condition between the nodes i,j or j,i


def Reliability(link_state,p):
    link_up_prob = np.array(link_state)*p
    swap = {0:1,1:0}
    inverting = lambda i: swap[i]
    link_dw_prob = np.array(list(map(inverting,link_state)))*(1-p)
    link = link_up_prob+link_dw_prob
    R = 1
    for i in link:
        R*=i # Calculate the reliability of the configuration
    return R

def DFS_algorithm(link_state,nodes):
    # Implements the DFS non-recursive algorithm
    stack = []    
    visited = []         # list that holds the visited nodes
    neighbour_nodes = [] # list that saves the neighbouring nodes 
    stack.append(nodes[0])
    neighbour_nodes.append(nodes[0])
    while(True):
        linked = False
        current_node = stack[-1]
        for i in nodes:
            temp = int((current_node+1)*(current_node+2)/2)
            if(link_state[current_node*len(nodes)+i-(temp)]==1 and (i not in neighbour_nodes) and (i>stack[-1])):
                stack.append(i)
                neighbour_nodes.append(i)
                linked = True
                
        if(linked==False):
            visited.append(stack.pop())
            
        if(not bool(stack)):
            break
    # if the length of visited list and nodes is equal then the graph is connected 
    if(len(visited)==len(nodes)):
        return True
    else:
        return False
    
def Total_reliability(K,p,k_gen):
    nodes = list(map(int,np.linspace(0,4,5)))
    R = 0
    n = 0
    for i in range(1024):
        
        # converting decimal number i to binary value 
        BIN = np.binary_repr(i,width=10)
        link_state = list(map(int,BIN))
        
        # applying DFS algorithm to check the conectivity of the graph
        condition = DFS_algorithm(link_state,nodes)
        
        if((i in K) and k_gen==True):
            condition = bool(~condition)
            
        if(condition==True):
            n+=1
            R += Reliability(link_state,p)
    return R

def K_var_fun():
    T = []
    p = 0.9
    k_samples = np.arange(0,26,1)
    k = 0
    while(k<=25):
        reliability = 0
        number_of_experiments = 10
        for i in range(number_of_experiments):
            samples = np.random.choice(range(1024),k,replace=False)
            reliability+=Total_reliability(samples,p,True)
            
        T.append(reliability/number_of_experiments)
        k+=1
    return T,k_samples

def P_var_fun():
    P = []
    h = 1
    p = np.arange(0,1.04,0.04)
    for t in p:
        k = np.random.choice(range(1024),h,replace=False)
        P.append(Total_reliability(k,t,True))
        
    return P,p

K,k = K_var_fun()
P,p = P_var_fun()
plt.figure()
plt.fill_between(k,0,K,edgecolor='r',lw=3)
plt.xticks(k)
plt.xlabel('$k$',fontsize=16)
plt.ylabel('$Total \ Reliability$',fontsize=16)
plt.title('$Total \ Reliability \ vs\ K$',fontsize = 16)
plt.grid()
plt.savefig('Total Reliability vs K plot 2.png')
plt.show()

plt.figure()
plt.plot(p,P)
plt.xlabel('$p$',fontsize=16)
plt.ylabel('$Total \ Reliability$',fontsize=16)
plt.title('$Total \ Reliability \ vs\ p$',fontsize = 16)
plt.savefig('Total Reliability vs p.png')
plt.show()