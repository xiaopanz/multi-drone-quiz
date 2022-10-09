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
Both time and space complexity is linear. For time complexity, it requires $O(M \times N)$ time. For space complexity, an $M \times N$ matrix is created to store the gird. 
### References
Bailey, D.(2004) _An Efficient Euclidean Distance Transform_. https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.107.5775&rep=rep1&type=pdf