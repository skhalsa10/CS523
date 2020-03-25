from p5 import *

# n = 200

# grid=[['s' for col in range(0,n)] for row  in range(0,n)]

# print(grid)
# def setup():
#     size(n*4,n*4)

# def draw():
#     background(0)
#     for row in range(0,n):
#         for col in range(0,n):
#             if grid[row][col] == 's':
#                 fill(0,128,0)
            
#             square((row*4, col*4),4)
            

# run()
from p5 import *

myArray = []
rows = None
columns = None

def setup():

        size(200, 200)
        global rows, columns, myArray
        columns = width
        rows = height

        for i in range(rows):
                myArray.append([])
                for j in range(columns):
                        myArray[i].append(int(random_uniform(255)))

def draw():
        global rows, columns, myArray
        for i in range(rows):
                for j in range(columns):
                        stroke(myArray[i][j])
                        point(i, j)

if __name__ == '__main__':
        run()