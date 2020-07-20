
from numpy import *

def generate_val():
    # The number of Nodes N = 20 
    # The traffic demand between the pair of nodes (i,j) is b_{i,j} 
    # The unit cost values for the link (i,j) is a_{i,j} 
    # bij = |di - dj|
    
    # the flow through the link 'd' 
    
    ID = '1210413658'
    ID = ID*2
    d = []
    
    for i in ID:
        d.append(int(i))
    
    
    # bij = |di - dj|
    b_ij = zeros([len(d),len(d)])
    
    for i in range(len(d)):
        for j in range(len(d)):
            if(i!=j):
                b_ij[i,j] = abs(d[i]-d[j])
            
            
    K = list(range(3,15))
    
    
    # A stores all the generated matrix of aij
    A = list()
    for k in K:
        a = zeros([len(d),len(d)])
        for i in range(len(d)):
            r = random.choice(len(d),k,replace=False)
            while(i in r):
                r = random.choice(len(d),k,replace=False)
        
            for j in range(len(d)):
                if(i!=j):
                    if(j in r):
                        a[i,j] = 1
                    
                    else:
                        a[i,j] = 100
                        
        A.append(a)
        
    return A,b_ij,K,d
    