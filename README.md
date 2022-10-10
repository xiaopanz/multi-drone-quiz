# multi-drone-quiz
## Problem 1
The code in main.py implements the idea from the paper _An Efficient Euclidean Distance Transform_.
The detailed implementation is described below.
### Implementation Detail
#### Row Scanning
The first step operates on each row independently. It consists of two passes – from left to right and then right to left. 
The initial distances of all points excepts obstacles in the grid is set to 999.
#### First Column Scanning
For each column, using a stack to track the influence of rows. 
Each stack item of contains a pair of values, representing respectively a row number, y, and the maximum row which that row influences.  
For each successive row, evaluated the influence by the following equation:  
$$y' = y_2 + {{I_2}^2 -{I_1}^2 - (y_2 - y_1)^2} \over 2(y_2 - y_1)$$

By the code:  
https://github.com/xiaopanz/multi-drone-quiz/blob/4910d2b239bff4d7ccf9c3ca898c5c404821672d/main.py#L52

There are three cases of interest:
1. $y′ > N$. The boundary of influence between $y_1$ and $y_2$ is past the end of the image, so the new row will have no influence. https://github.com/xiaopanz/multi-drone-quiz/blob/4910d2b239bff4d7ccf9c3ca898c5c404821672d/main.py#L53-L54
2. $y′ > {y_0}^I$, where ${y_0}^I$ is the influence from the previous stack entry.  In this case row $y_1$ has a range of influence, and $y_I$ is set to y′ . The new row, $y_2$ is added to the stack. https://github.com/xiaopanz/multi-drone-quiz/blob/4910d2b239bff4d7ccf9c3ca898c5c404821672d/main.py#L55-L56
3. $y' <= {y_0}^I$. $y_1$ has no influence on this column, therefore pop it off the top of the stack. Repeated the steps before until either stack is empty or case 2 is met. https://github.com/xiaopanz/multi-drone-quiz/blob/4910d2b239bff4d7ccf9c3ca898c5c404821672d/main.py#L57-L64

#### Second Column Scanning
Perform a seconding column scanning based on the stack of influences to evaluate the distances. 

https://github.com/xiaopanz/multi-drone-quiz/blob/4910d2b239bff4d7ccf9c3ca898c5c404821672d/main.py#L66-L76

### Complexity Analysis
Both time and space complexity are linear. For time complexity, it requires $O(M \times N)$ time. For space complexity, an $M \times N$ matrix is created to store the gird. 
### References
Bailey, D.(2004) _An Efficient Euclidean Distance Transform_. https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.107.5775&rep=rep1&type=pdf

##Problem 2
### Implementation Idea
Since we only need to calculate the distance to the nearest obstacle for each drone. we can use the Euclidean Distance Transform algorithm implemented 
in the Problem 1. We can create a distance grid which store all obstacles locations and calculate the distance grid for the map. Then in each timestamp, we can just
lookup the distance grid for each drone's updated position.

### Complexity Analysis
Both time and space complexity are linear. 
Suppose the map consists M rows and N columns, with x drones.
For time complexity, it requires $O(x \times M \times N)$ time for the first timestamp, then $O(x) time for the rest of time. 
For space complexity, an $M \times N$ matrix is created to store the map. 

## Problem 3
### Implementation Idea
If we want to calculate the distances to K nearest obstacles, we can reuse the stack of paired value from the algorithm implemented in Problem 1.
For each column, the stack record the row number and its influence for that column.  
This time, instead of only calculating the distance from the top of stack for the row number and its influence, 
we can use the top k elements on the stack.
It will give us the result of the distances to K nearest obstacles.
### Complexity Analysis
Both time and space complexity are still linear. 
Suppose the map consists M rows and N columns, with x drones.
For time complexity, it requires $O(x \times M \times N)$ time for the first timestamp, then $O(x) time for the rest of time. 
For the second pass of column scanning, it will take $K\times M \times N) time. Since K is always less than x, it would increase the time complexity.

## Problem 4

### Implementation Idea
For the $10\times 10\times 10$ space, we can apply the Octree Space Partitioning (OSP)  to 
recursively subdivide the 3D space and then place the box into the space using DFS.  
Firstly, sort the boxes by their size, then placing the largest box into one corner of the space. Fill 
in the corresponding nodes in the octree. In order to improve the performance, if the box occupied the entire space of
one node, only fill in this node and skip the children of this node.  
Then we can perform a depth first search for the rest of the boxes, sorted in the descending order of size. For each box,
go to the level of the Octree where length equals to the longest length of three-dimensional values. Then fill the nodes
according to the value of the other two dimensions. Finally, either all boxes are put in the Octree, or
there is no enough space for some boxes.

