import numpy as np

# Generation of the uniform random sequence

def uniform():
    k  = 16807
    so = 1111
    m  = 2147483647    
    while(1):
        
        s = (k*so)%m
        r = s/m
        so = s
        yield r

uni = uniform()
def expo_rand(lamb):
    # The generation of exponential random varaible
    
    y = (-1/lamb)*np.log(uni.__next__())
    return y
