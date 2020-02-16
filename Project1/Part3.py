# Part 3: Figure 3 code that measures Top Down and Bottom Up Transfer Entropies (TE) for different epsilons.
# For each epsilon value, we selected 10 different Meta-Populations (Mean, M_n) and 3 random Sub-Populations within
# each meta-population. We averaged the TE's and statistically show the relationship between them.
# Implementated by Anas Gauba
import matplotlib.pyplot as plt
import numpy as np
import JIDTTransferEntropy as jidt

#equation 1 on page 4 called model
n = 10000
N = 1000
epselons = [0, 0.075, 0.1, 0.2, 0.225, 0.25, 0.3, 0.4, 0.6, 0.7, 0.9, 1]
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
topDownTE = np.zeros((30, len(epselons)))
bottomUpTE = np.zeros((30, len(epselons)))
bins = list(range(0,100)) # we have numbers between 0 and 100 for our data.

meanTopDownTE = np.zeros(len(epselons))
standardDevTopDownTE = np.zeros(len(epselons))

meanBottomUpTE = np.zeros(len(epselons))
standardDevBottomUpTE = np.zeros(len(epselons))

# difference between Bottom Up and Top Down.
differenceTE = np.zeros(len(epselons))

for e in epselons:
    metaPopulations = np.zeros((n, 10))
    subPopulations = np.zeros((n,10*3))
    entropyCount = 0

    # PART 3: 
    # for each epsilon, there will be 10 runs for metapopulations and in each metapopulation, we randomly choose 3
    # choose 3 subpopulations.
    for i in range(0,10):
        # Can also save the meta and subpopulation data to a file to manually plug into JIDT tool.
        # Although I don't recommend it since I have exported the JIDT tool to automate the calculation process of TE.
        # In case you need to see it, just uncomment the code for saving to file. 
        
        # fileToSave = open("transfer_entropy_data_e_" + str(e) + "_meta_" +str(i+1)+ ".txt", "w")
        # fileToSave.write("%% The data is of form: M_i sub(1) sub(2) sub(3)\n")
        
        build_xs(xs_i_n, K, N, e)
        M_ns = np.zeros(n)

        for j in range(0, n):
            M_ns[j] = M_n(xs_i_n[:, j], N)

        metaPopulations[:,i] = np.digitize(M_ns, bins)

        # 3 random subpopulations for each metapopulation.
        subPopulations[:,i] = np.digitize(xs_i_n[np.random.randint(0,N),:], bins)
        subPopulations[:,i+1] = np.digitize(xs_i_n[np.random.randint(0,N),:], bins)
        subPopulations[:,i+2] = np.digitize(xs_i_n[np.random.randint(0,N),:], bins)

        # call JIDT tool's code for calculating TopDown transfer entropy.
        topDownTE[entropyCount, epsItr] = jidt.calculateTransferEntropy(metaPopulations[:,i], subPopulations[:,i])
        topDownTE[entropyCount+1, epsItr] = jidt.calculateTransferEntropy(metaPopulations[:,i], subPopulations[:,i+1])
        topDownTE[entropyCount+2, epsItr] = jidt.calculateTransferEntropy(metaPopulations[:,i], subPopulations[:,i+2])

        # call JIDT tool's code for calculating BottomUp TE.
        bottomUpTE[entropyCount, epsItr] = jidt.calculateTransferEntropy(subPopulations[:,i], metaPopulations[:,i])
        bottomUpTE[entropyCount+1, epsItr] = jidt.calculateTransferEntropy(subPopulations[:,i+1], metaPopulations[:,i])
        bottomUpTE[entropyCount+2, epsItr] = jidt.calculateTransferEntropy(subPopulations[:,i+2], metaPopulations[:,i])

        entropyCount += 3

        # for k in range(0,n):
        #     fileToSave.write(str(int(metaPopulations[k,i])) + " " + str(int(subPopulations[k,i]))
        #      + " " + str(int(subPopulations[k,i+1])) + " " + str(int(subPopulations[k,i+2])) + "\n")            

        # fileToSave.close() 

    # now average both the topDown TE and bottomUP TE.
    meanTopDownTE[epsItr] = np.mean(topDownTE[:,epsItr])
    meanBottomUpTE[epsItr] = np.mean(bottomUpTE[:,epsItr])

    # standard deviation
    standardDevTopDownTE[epsItr] = np.std(topDownTE[:,epsItr])
    standardDevBottomUpTE[epsItr] = np.std(bottomUpTE[:,epsItr])

    differenceTE[epsItr] = meanBottomUpTE[epsItr] - meanTopDownTE[epsItr]

    epsItr += 1

    #print("This is meta: \n", metaPopulations)
    #print("This is sub: \n", subPopulations)


# plot here:
plt.xlabel("Global coupling strength (epsilons)")
plt.ylabel("Transfer Entropy (bits)")
plt.title("Top Down and Bottom Up Causation")

plt.plot(epselons, meanTopDownTE, lw=2, label='Top Down TE', color='blue')
plt.plot(epselons, meanBottomUpTE, lw=2, label='Bottom Up TE', color='black', ls='--')
plt.plot(epselons, differenceTE, lw=2,label= 'Difference b/w Bottom Up and Top Down', color='red')
leg = plt.legend(loc='upper right', prop={'size':7})

plt.fill_between(epselons, meanTopDownTE+standardDevTopDownTE, meanTopDownTE-standardDevTopDownTE, facecolor='blue', alpha=0.5)
plt.fill_between(epselons, meanBottomUpTE+standardDevBottomUpTE, meanBottomUpTE-standardDevBottomUpTE, facecolor='black', alpha=0.5)

# filling between the difference of bottom up to top down to statistically show 
# when bottom up is significantly high and when top down is high. 
plt.fill_between(epselons, 0, differenceTE, where= differenceTE > 0, facecolor='red', alpha=0.5)
plt.fill_between(epselons, 0, differenceTE, where= differenceTE < 0, facecolor='yellow', alpha=0.5)

plt.show()
