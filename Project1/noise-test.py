from p5 import noise as noise
from p5 import remap as remap
import p5
import numpy as np
import matplotlib.pyplot as plt


xs = np.zeros(100)
rs = np.zeros(100)
random_rs = np.zeros(100)

t = 0
for i in range(0,100):
    xs[i] = noise(t)
    random_rs[i] = np.random.uniform(3.9, 4.0)
    t += 0.01

# print(remap(.5,(0,1),(3.9,4)))
for i in range(0,100):
    rs[i] = remap(xs[i],(0,1),(3.9,4))

p5.noise_seed(1300000)
print(remap(noise(1/100),(0,1),(3.9,4)))
p5.noise_seed(7)
print(noise(1/100))
print(101/100)
p5.noise_seed(0)
print(noise(0))
p5.noise_seed(7)
print(noise(0))
for i in range (0, 1000):
    p5.noise_seed(i)
    print(remap(noise(i/100),(0,1),(3.9,4)))


# plt.plot(range(0,100), rs,label="perlin noise")
# plt.plot(range(0,100),random_rs,label="random")
# plt.title("Perlin Noise vs random number genertor")
# plt.xlabel("Time Steps")
# plt.ylabel("R")
# plt.legend()
# plt.show()    

