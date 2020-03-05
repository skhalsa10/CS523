from random import randint
from copy import deepcopy

#  some inputs for the 1d dense check

###dense_0 contains 151 '0' and 50 '1' ###
dense_0 = ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1', '0', '1', '0', '0', '1']
### dense_1 contains 151 1s and 50 0s ###
dense_1 = ['1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1', '0', '1', '1', '1', '0', '0', '1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '0', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '0', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '0']

rule_399 = {0: '0', 1: '0', 2: '0', 3: '1', 4: '0', 5: '0', 6: '0', 7: '0', 8: '0', 9: '0', 10: '1', 11: '0', 12: '1', 13: '1', 14: '1', 15: '1', 16: '0', 17: '0', 18: '0', 19: '1', 20: '1', 21: '0', 22: '1', 23: '1', 24: '0', 25: '0', 26: '0', 27: '0', 28: '1', 29: '1', 30: '0', 31: '0', 32: '0', 33: '1', 34: '1', 35: '0', 36: '0', 37: '1', 38: '0', 39: '1', 40: '1', 41: '1', 42: '1', 43: '1', 44: '0', 45: '0', 46: '0', 47: '1', 48: '1', 49: '0', 50: '0', 51: '0', 52: '0', 53: '1', 54: '1', 55: '1', 56: '0', 57: '0', 58: '1', 59: '1', 60: '0', 61: '0', 62: '0', 63: '1', 64: '0', 65: '1', 66: '0', 67: '1', 68: '0', 69: '0', 70: '0', 71: '0', 72: '1', 73: '0', 74: '1', 75: '0', 76: '0', 77: '1', 78: '0', 79: '0', 80: '0', 81: '0', 82: '0', 83: '1', 84: '1', 85: '0', 86: '0', 87: '0', 88: '1', 89: '0', 90: '0', 91: '0', 92: '1', 93: '1', 94: '0', 95: '0', 96: '0', 97: '0', 98: '1', 99: '1', 100: '0', 101: '0', 102: '0', 103: '0', 104: '1', 105: '0', 106: '1', 107: '1', 108: '0', 109: '0', 110: '1', 111: '1', 112: '0', 113: '0', 114: '1', 115: '1', 116: '0', 117: '1', 118: '1', 119: '1', 120: '1', 121: '0', 122: '0', 123: '1', 124: '0', 125: '0', 126: '1', 127: '1'}
testrule = {'fitness': 201, 0: '0', 1: '0', 2: '0', 3: '0', 4: '0', 5: '1', 6: '0', 7: '0', 8: '0', 9: '1', 10: '1', 11: '0', 12: '0', 13: '1', 14: '0', 15: '0', 16: '0', 17: '1', 18: '1', 19: '1', 20: '0', 21: '0', 22: '0', 23: '1', 24: '0', 25: '0', 26: '0', 27: '0', 28: '1', 29: '1', 30: '1', 31: '1', 32: '0', 33: '0', 34: '0', 35: '0', 36: '0', 37: '0', 38: '1', 39: '1', 40: '0', 41: '0', 42: '0', 43: '1', 44: '0', 45: '1', 46: '0', 47: '0', 48: '1', 49: '0', 50: '0', 51: '0', 52: '1', 53: '1', 54: '1', 55: '0', 56: '0', 57: '1', 58: '0', 59: '1', 60: '0', 61: '0', 62: '0', 63: '1', 64: '0', 65: '0', 66: '0', 67: '0', 68: '0', 69: '1', 70: '0', 71: '1', 72: '0', 73: '0', 74: '0', 75: '0', 76: '1', 77: '1', 78: '1', 79: '1', 80: '0', 81: '0', 82: '0', 83: '0', 84: '0', 85: '1', 86: '0', 87: '0', 88: '1', 89: '0', 90: '0', 91: '1', 92: '1', 93: '1', 94: '0', 95: '1', 96: '0', 97: '1', 98: '0', 99: '0', 100: '0', 101: '1', 102: '0', 103: '0', 104: '0', 105: '1', 106: '1', 107: '1', 108: '1', 109: '1', 110: '0', 111: '0', 112: '0', 113: '1', 114: '1', 115: '0', 116: '1', 117: '0', 118: '1', 119: '0', 120: '0', 121: '1', 122: '0', 123: '0', 124: '0', 125: '0', 126: '0', 127: '1'}


dense_0_75 = []
dense_1_75 = []

# build an array of '0's
all_0 = []
all_1 = []

for i in range(0,201):
    all_0.append('0')
    all_1.append('1')


minority_count_for0 = 0
minority_count_for1 = 0
for i in range(0,75):
    temp_0 = deepcopy(all_0)
    temp_1 = deepcopy(all_1)
    
    
    
    while(minority_count_for0 >0):
        ind_for0 = randint(0,200)
        if(temp_0[ind_for0] == '0'):
            temp_0[ind_for0] = '1'
            minority_count_for0 -= 1

    while(minority_count_for1 >0):
        ind_for1 = randint(0,200)
        if(temp_1[ind_for1] == '1'):
            temp_1[ind_for1] = '0'
            minority_count_for1 -= 1
    
    dense_0_75.append(deepcopy(temp_0))
    dense_1_75.append(deepcopy(temp_1))

    minority_count_for0 += 2*i
    minority_count_for1 += 2*i


