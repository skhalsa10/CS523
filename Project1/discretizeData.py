# The concept of Discretization: https://www.youtube.com/watch?v=MK_dMsn4MqI
import numpy as np

# data: list of populations in real numbers. 
# steps: discrete number representing percentage/groups in which we want the data elements to map to.
def discretize(data, steps):
    threshold = []
    stepSize = np.size(data)/steps
    data.sort()
    for i in range(0, steps):
        print(data[i+1]*stepSize)
        threshold.append(data[i+1]*stepSize)
    
    return threshold
