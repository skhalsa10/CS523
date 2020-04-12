# This Project utilizes Processing p5 library. 
# API and setup instructions: https://p5.readthedocs.io/en/latest/install.html#prerequisites-python
# 
# In this project I will attempt to replicate Mitchels 1d density GA cellular automota
# it will converge to either all 1's or all 0's based on if the inititial 
# condition has a greater density of 1's or 0'sin the case of this application 
# 1's will be rendered as black and 0's will be rendered as white

import numpy as np

### Example 1d Cellular Automata using a specific rule. 

# Inital condition bit pattern array.
arr = [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0]

# array in the next time step.
nextArr = list(np.zeros(len(arr)))

# Example Dictionary for a specific rule. Wolfram's Rule 110
rule110 = {
    "000": 0,
    "001": 1,
    "010": 1,
    "011": 1,
    "100": 0,
    "101": 1,
    "110": 1,
    "111": 0
}

# Run for 100 generations/timesteps.
print(arr)
for i in range(0,100):

    for j in range(0, len(arr)):
        # Temp variable to access the array.     
        bitPattern = str(arr[j-1])+str(arr[j])+str(arr[(j+1) % len(arr)])
        nextArr[j] = rule110[bitPattern]
    temp = arr
    arr = nextArr
    nextArr = temp    
    
    print(arr)


from p5 import *

x = 0

def setup():
    size(800,800)
    no_stroke()
    background(255)

def draw():

    global x
    if  mouse_is_pressed:
        fill(0)
    else:
        fill(255)
    # ellipse((x,50),20,20,mode=RADIUS)
    square((x,50),4)
    x += 1
    if x>width:
        x=0
    #print(x)

    




if __name__ == '__main__':
    run()


