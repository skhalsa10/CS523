# This Project utilizes Processing p5 library. 
# API and setup instructions: https://p5.readthedocs.io/en/latest/install.html#prerequisites-python
# 
# In this project I will attempt to replicate Mitchels 1d density GA cellular automota
# it will converge to either all 1's or all 0's based on if the inititial 
# condition has a greater density of 1's or 0'sin the case of this application 
# 1's will be rendered as black and 0's will be rendered as white

from p5 import *

x = 0

def setup():
    size(480, 120)

def draw():
    background(50)
    global x
    if  mouse_is_pressed:
        fill(0)
    else:
        fill(255)
    ellipse((x,50),20,20,mode=RADIUS)
    x += 1
    if x>width:
        x=0
    print(x)

    




if __name__ == '__main__':
    run()


