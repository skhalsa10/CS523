# Part 2: Figure 2 Code that shows the behavior of different populations behaving differently by making
# a pattern based on different epsilons (coupling strength).
# Implementation Details: both by Anas Gauba and Siri Khalsa.

import matplotlib.pyplot as plt
import numpy as np

#equation 1 on page 4 called model
n = 10000
N = 1000
epselons = [0, 0.075, 0.1, 0.2, 0.225, 0.25, 0.3, 0.4]
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



for e in epselons:
    build_xs(xs_i_n, K, N, e)
    M_ns = np.zeros(n)

    for i in range(0, n):
        M_ns[i] = M_n(xs_i_n[:, i], N)

    s = plt.scatter(M_ns[0:n - 1], M_ns[1:n], s=.1, marker='*', label = 'e ='+str(e))

plt.xlabel("M_n")
plt.ylabel("M_n+1")
plt.plot(range(0, 100), range(0, 100), linewidth=.1, color='black')
plt.legend()
plt.title("Bottom-up to Top-down Causation")
plt.xlim(40,80)
plt.ylim(40,80)
plt.show()
