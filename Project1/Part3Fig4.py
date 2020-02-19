# Part 3: Figure 4 code that measures the mutual information among subpopulations for e=0.075 with other values
# of epsilon. 
# Implemented by Anas Gauba

import matplotlib.pyplot as plt
import numpy as np
import JIDTMutualInfo as jidt

#equation 1 on page 4 called model
n = 10000
N = 1000
# Compare Mutual Info of subpopulations at epsilon 0.075 vs maybe 3 others. 
epselons = [0, 0.075, 0.1, 0.2, 0.25, 0.3, 0.4, 0.6, 0.7, 0.9, 1]
#epselons = [0, 0.075, 0.25, 0.4, 0.6, 1]
K = 100

# the goal here is to build a matrix with N rows and n column
# here the first row will be all the x_0_n
xs_i_n = np.zeros((N, n))
xs_i_n[:, 0] = 1  # per the paper will start out everything at 1 when n = 0


def getRandomR():
    return np.random.uniform(3.9, 4.0)


#logistic growth law
def f(x, K):
    r = getRandomR()
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
def m_n(x_js, N, K):
    sum = 0

    for x_j in x_js:
        sum += f(x_j, K)

    return sum / N


# I will go column by column in xs_i_n starting at column 1 which relies on column 0
def build_xs(xs_i_n, K, N, e):
    for column in range(1, n):
        #first get the little m of previous column and cache it
        m_n_cache = m_n(xs_i_n[:, column - 1], N, K)

        for row in range(0, N):
            xs_i_n[row][column] = (1 - e) * f(xs_i_n[row][column - 1], K,) + e * m_n_cache



epsItr = 0
mutualInfo = np.zeros((N-1,len(epselons)))
meanMutualInfo = np.zeros(len(epselons))

bins = list(range(0,100)) # we have numbers between 0 and 100 for our data.

for e in epselons:
    # metaPopulations = np.zeros((n, 10))
    # all N logistic maps subpopulations for each epsilon.
    subPopulations = np.zeros((n,N))

    build_xs(xs_i_n, K, N, e)
    # M_ns = np.zeros(n)

    # for j in range(0, n):
    #     M_ns[j] = M_n(xs_i_n[:, j], N)

    miCount = 0
    subPopulations[:,0] = np.digitize(xs_i_n[0,:], bins)
    subPopulations[:,1] = np.digitize(xs_i_n[1,:], bins)

    for i in range(2,N):
        subPopulations[:,i] = np.digitize(xs_i_n[i,:], bins)

        mutualInfo[miCount, epsItr] = jidt.calculateMutualInfo(subPopulations[:,i-2], subPopulations[:,i-1])
        miCount += 1

        # the last computation.
        if (i == N-1):
            mutualInfo[miCount, epsItr] = jidt.calculateMutualInfo(subPopulations[:,i-1], subPopulations[:,i])

    #print(mutualInfo[:,epsItr])
    #plt.plot(range(0,N-1), mutualInfo[:,epsItr], label='epsilon = ' + str(e))
    meanMutualInfo[epsItr] = np.mean(mutualInfo[:, epsItr])
    epsItr += 1
    
# plot bar graph
epselons = list(map(lambda x: str(x),epselons))
plt.bar(epselons, list(meanMutualInfo), align='center',width=0.3,alpha=0.5)
#plt.xticks(epselons)
plt.xlabel("epsilons (e)")
plt.ylabel("Mutual Information (MI)")
plt.title("Comparing MI among subpopulations for e=0.075\n and other epsilon values")
#plt.legend()
plt.show()