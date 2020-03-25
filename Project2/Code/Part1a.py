from math import factorial
### I will generate some functions to calculate the number of RNA strands###


### k is number of mutations away 
### n is the number of nucliotides in RNA
### k MUST be less than n
def calc_K_Mutations_Away(k,n):
    return (3**k)*(factorial(n)//(factorial(k)*factorial(n-k)))

def total_possible_mutations(n):
    total = 0
    for k in range(0,n+1):
        total += calc_K_Mutations_Away(k,n)

    return total

print(calc_K_Mutations_Away(1,30000))