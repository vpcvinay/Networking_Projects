## Overview ##
Graph orientation is an algorithm that calculates and assigns directional links to an undirected graph such that, the maximum outdegree of the graph is minimized. The algorithm take linear time complexity *O(N)* (where N is the total number of links) and *O(N<sup>2</sup>)* space complexity and works on complete or incomplete graphs. The correctness of the algorithm is demostrated by applying it to the complete and incomplete graphs and the output is verified.

The module is written using Python 3.2 Jupyter Notebook environment.

## Algorithm
The program takes an integer representing the number of nodes for a complete graph and for the incomplete graph, it takes two arguments such as the number of nodes, and graph matrix representing the links. The graph matrix is a list of lists consisting of 1's representing outward link, 0's representing the inward link and -1's representing no link between the source and the destination. The algorithm iterates over all the links and calculates the inward and outward degree of the source and destination and inverts the link states if the outdegree or indegree is grater than the maximum allowed which is represented by |N/n| ('N' is the number of links and 'n' is the number of nodes). The output of the program is a matrix of the directional graph containing 1's and 0's. For more information of the algorithm refer the document "Graph orientation problem.pdf".

## Running Instructions
```
$ python
```
This opens the python interpreter and follow the commands;

```
>>> import orientation as orient
>>> no_of_nodes = 4
>>> Graph = orient.graph_orientation(no_of_nodes = no_of_nodes)
>>> Graph.all_connected = True
>>> Graph.construct_graph()
>>> Graph.graph
```
This solves the orientation of the complete undirected graph and the output would be;

```
array([[-1.,  0.,  0.,  1.],
       [ 1., -1.,  0.,  0.],
       [ 1.,  1., -1.,  0.],
       [ 0.,  1.,  1., -1.]])
```
For incomplete graph;

```
>>> no_of_nodes = 4
>>> graph = np.array([[-1, 0, 0, -1], 
>>>                   [0, -1, -1, 0], 
>>>                   [0, -1, -1, 0],
>>>                   [-1, 0, 0, -1]])
>>> Graph = orient.graph_orientation(graph=graph, no_of_nodes = no_of_nodes)
>>> Graph.all_connected = False
>>> Graph.construct_graph()
>>> Graph.graph

array([[-1,  0,  1,  0],
       [ 1, -1,  0,  0],
       [ 0,  0, -1,  1],
       [ 0,  1,  0, -1]])
 ```
