Walk Router
==========================
Installation
------------
Python 3.7.0+ is required because of using ``dataclasses``.  
Install the only third-party dependency ``click`` – used for building Command Line Interface:

    pip install click

Usage
-----

    ./run.sh <path_to_graph_file> <from_node_id> <to_node_id>

or

    python src/main.py <path_to_graph_file> <from_node_id> <to_node_id>

Example:

    ./run.sh citymapper-coding-test-graph.dat 876500321 1524235806
    2709
    
Rationale
---------
When it comes to solving shortest path problem the first algorithm that comes to mind is Dijkstra’s.  
But since this is a single-source shortest path algorithm, which means that we’re searching for shortest paths from initial node to all other nodes, 
I gave a thought to A* algorithm since it solves single-pair shortest path problem and makes it slightly faster than Dijkstra’s because of using heuristics.  
So far as A*’s heuristics work best on grid-like graphs and we can’t be sure that our graph will always meet this requirement, 
I decided to focus on implementation of Dijkstra’s, assuming that we’ll have only non-negative weights of edges.  
As for implementation, I sticked to algorithm with the use of priority queue to reduce the time on choosing nearest adjacents in a graph, 
also since we are searching for a single-pair shortest distance, we can stop the algorithm once the destination node is reached.

Improvements
------------
Depending on the requests rate to application and the size of graph, current solution could be extended and improved in different ways.
Just to mention a few:

First of all, we can save some time on graph building 
simply by pickling built graph at the end of script run, 
and by unpickling it at the start of the new run (if graph file hasn't changed). 

Suppose we have the same graph most of the time with the same size as in the task, but we want to minimise the response time as much as possible.   
In this case we can use one of the all-pairs shortest path algorithms (Johnson’s algorithm or Dijkstra’s run on each node, for example) to precompute all-pairs shortest distances
and store that data on disc (could be also stored in RAM if we’ve had backend app with API). 
The initial run of the app will take time to precompute all-pairs shortest distances, 
but next runs will take much less time because of the precomputation made – most of the time will be spent on deserialisation of precomputed distances. 
The precomputation step may also be sped up by parallelisation of the algorithm.

In case if the graph and it’s size changes over time and grows big, precomputation won’t help us much. 
For this I’d choose to run bidirectional Dijkstra’s from both of the nodes in parallel. 
LRU cache can be used here to store top of requested distances to avoid their recomputation.
