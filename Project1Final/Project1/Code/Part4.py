# Part 2: Figure 2 Code that shows the behavior of different populations behaving differently by making
# a pattern based on different epsilons (coupling strength).
# Implementation Details: both by Anas Gauba and Siri Khalsa.

# The idea behind problem 4 is to critisize the random sabling of r at every time step.
# It does seem that r should change: however a random change seems to be the wrong approach. 
# a More appropriate approach should be something that changes slow and gradually. A perlin noise 
# could support a more natural change to r over time  we will explore this for part 4

import matplotlib.pyplot as plt
import numpy as np
from p5 import remap as remap
import p5

#equation 1 on page 4 called model
n = 10000
N = 1000
epselons = [0, 0.075, 0.1, 0.2, 0.225, 0.25, 0.3, 0.4]
K = 100


# the goal here is to build a matrix with N rows and n column
# here the first row will be all the x_0_n
xs_i_n = np.zeros((N, n))
xs_i_n[:, 0] = 1  # per the paper will start out everything at 1 when n = 0
rs = np.zeros((N, n))


def getRandomR():
    return np.random.uniform(3.6, 3.7)

def build_rs():
    #convenient way to build a list of random Rs that has length N
    rseed = list(map(lambda x: np.random.uniform(0,13000),np.zeros(N)))
    for row in range(0,N):
        p5.noise_seed(rseed[row])
        for col in range(0,n):
            rs[row][col] = remap(p5.noise(col/100),(0,1),(3.9, 4.0))

build_rs()

print(rs)






#logistic growth law
def f(x,r, K):
    return (r * x * (1 - (x / K)))



#instantatneous Mean field states
#this should take in a list of all x_j at generation n
# this essentially takes the average of a column in the xs_i_n matrix
def M_n(x_js, N):
    return sum(x_js) / N


#instantatneous Mean field dynamics
# instead of averaging the values of the x_js at a given generation n
# this function will take the average of the logistic growth of
# all the x_js at a given generation
###### added col to this function to be used for noise function for the rs
def m_n(x_js, N, K,col):
    sum = 0
    # for x_j in x_js:
    #     sum += f(x_j, K)
    # need the index to get appropriate r converting thisto a different version
    for row in range(0, len(x_js)):
        
        sum += f(x_js[row],rs[row][col],K)

    return sum / N


# I will go column by column in xs_i_n starting at column 1 which relies on column 0
def build_xs(xs_i_n, K, N, e):
    for col in range(1, n):
        #first get the little m of previous column and cache it
        m_n_cache = m_n(xs_i_n[:, col - 1], N, K, (col - 1))

        for row in range(0, N):
            
            xs_i_n[row][col] = (1 - e) * f(xs_i_n[row][col - 1],rs[row][col],K) + e * m_n_cache



for e in epselons:
    print(e)
    build_xs(xs_i_n, K, N, e)
    M_ns = np.zeros(n)

    for i in range(0, n):
        M_ns[i] = M_n(xs_i_n[:, i], N)

    s = plt.scatter(M_ns[0:n - 1], M_ns[1:n], s=.1, marker='*',linewidth=.3,label = 'e ='+str(e))

plt.xlabel("M_n")
plt.ylabel("M_n+1")
plt.plot(range(0, 100), range(0, 100), linewidth=.1, color='black')
leg = plt.legend(loc='lower left',markerscale=12)

plt.title("R in range [3.9, 4.0]")
# plt.xlim(40,80)
# plt.ylim(40,80)
plt.show()
