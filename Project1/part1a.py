import matplotlib.pyplot as plt
import numpy as np

#Part 1 figure1a
r1 = 2.9 # to analyze non chaotic behavior.
r2 = 3.9 # to analyze chaotic behavior
timesteps = 100

xnot_r1_1 = 0.3
xnot_r1_2 = 0.300000001
xnot_r2_1 = 0.6
xnot_r2_2 = 0.600000001

# init and declare lists to store x vals 
xval_r1_1 = list(np.zeros(timesteps))
xval_r1_2 = list(np.zeros(timesteps))
xval_r2_1 = list(np.zeros(timesteps))
xval_r2_2 = list(np.zeros(timesteps))

# init xnot for each xval list
xval_r1_1[0] = xnot_r1_1
xval_r1_2[0] = xnot_r1_2
xval_r2_1[0] = xnot_r2_1
xval_r2_2[0] = xnot_r2_2

def logistic_map(x,r):
    return r*x*(1-x)

# populate vals  r1_1
for i in range(1,timesteps):
    x = xval_r1_1[i-1]
    xval_r1_1[i] = logistic_map(x,r1)

# populate vals  r1_2
for i in range(1,timesteps):
    x = xval_r1_2[i-1]
    xval_r1_2[i] = logistic_map(x,r1)

# populate vals  r2_1
for i in range(1,timesteps):
    x = xval_r2_1[i-1]
    xval_r2_1[i] = logistic_map(x,r2)

# populate vals  r2_2
for i in range(1,timesteps):
    x = xval_r2_2[i-1]
    xval_r2_2[i] = logistic_map(x,r2)

# okay now it is time to graph!
fig1 = plt.figure()
plt.plot(range(0,timesteps),xval_r1_1, label= 'initial x = 0.3')
plt.plot(range(0,timesteps),xval_r1_2,'--', label= 'initial x = 0.300000001')
plt.xlabel('Timesteps')
plt.ylabel('Population')
plt.title('logistic Map with R=2.9 ')
plt.legend()
# The key points here are to show that when we have a logistic map
#  with an R that leads to a fixed point attractor then there is
#  not much sensitivity to initial conditions.

fig1 = plt.figure()
plt.plot(range(0,timesteps),xval_r2_1, label= 'initial x = 0.6')
plt.plot(range(0,timesteps),xval_r2_2,'--', label= 'initial x = 0.600000001')
plt.xlabel('Timesteps')
plt.ylabel('Population')
plt.title('logistic Map with R=3.9 ')
plt.legend()
# Now compare the first graph to the second graph with an R that 
# leads to an infinity attractor or chaos. we have initial values 
# that have the same distance from eachother as above. they stay 
# close for about 20 iterations where they change drastically.this 
# emphasizes sensitivity to initial conditions.

plt.show()