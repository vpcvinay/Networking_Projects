
import numpy as np

class graph_orientation:
    def __init__(self, graph=np.zeros(1), no_of_nodes=2):
        
        self.no_of_nodes = no_of_nodes
        self.graph = graph
        self.N = int(((self.no_of_nodes*(self.no_of_nodes-1)/2))+0.5)
        self.min_out_degree = int((self.N/self.no_of_nodes)+0.5)
        self.out_degree = np.zeros(self.no_of_nodes)
        self.in_degree = np.zeros(self.no_of_nodes)
        self.all_connected = True
        self.link_state = np.zeros(self.N)
        
    def update_graph(self,i,j,l):       
        swap = {0:1,1:0}
        inverting = lambda t: swap[t]
        
        if(self.out_degree[i]+self.link_state[l]>self.min_out_degree or
           self.in_degree[i]+inverting(self.link_state[l])>self.min_out_degree):
            self.link_state[l] = inverting(self.link_state[l])
        else:
            self.out_degree[i]+=self.link_state[l]
            self.in_degree[i]+=inverting(self.link_state[l])
        
        if(self.out_degree[j]+inverting(self.link_state[l])>self.min_out_degree or
           self.in_degree[j]+self.link_state[l]>self.min_out_degree):
            self.link_state[l] = inverting(self.link_state[l])
            
        else:
            self.out_degree[j]+=inverting(self.link_state[l])
            self.in_degree[j]+=self.link_state[l]
            

    def construct_graph(self):
        if(self.all_connected==True):
            self.graph = np.zeros((self.no_of_nodes,self.no_of_nodes))
            swap = {0:1,1:0}
            inverting = lambda t: swap[t]
            i,j = 0,0
            for l in range(self.N):
                if(j==self.no_of_nodes-1):
                    i+=1
                    
                j = int((l+(i+1)*(i+2)/2)%self.no_of_nodes)
                self.update_graph(i,j,l)
                self.graph[i][j] = self.link_state[l]
                self.graph[j][i] = inverting(self.link_state[l])
                
                
        else:
            swap = {0:1,1:0}
            inverting = lambda t: swap[t]
            i,j = 0,0
            self.no_of_links = 0
            for l in range(self.N):
                if(j==self.no_of_nodes-1):
                    i+=1
                    
                j = int((l+(i+1)*(i+2)/2)%self.no_of_nodes)
                self.link_state[int(i*self.no_of_nodes+j-((i+1)*(i+2)/2))] = self.graph[i][j]
                if(graph[i][j]!=-1):
                    self.no_of_links+=1
                    
            i,j = 0,0
            self.min_out_degree = int((self.no_of_links/self.no_of_nodes)+0.5)
            
            for l in range(self.N):
                if(j==self.no_of_nodes-1):
                    i+=1
                j = int((l+(i+1)*(i+2)/2)%self.no_of_nodes)
                if(self.link_state[l]==-1):
                    self.graph[i][j],self.graph[j][i] = 0,0
                    continue
                
                self.update_graph(i,j,l)
                self.graph[i][j] = self.link_state[l]
                self.graph[j][i] = inverting(self.link_state[l])
        
                