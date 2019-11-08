"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""

from tqdm import tqdm
import random
import math
import matplotlib.pyplot as plt
from statistics import mean


class Set:
    def __init__(self, elements):
        '''sets have two attributes, elements and the sum of those elements'''
        self.elements = elements
        self.sum = sum(self.elements)

    def __lt__(self,other):
        '''compare sets based on their sum'''
        return self.sum < other.sum

    def __add__(self,other):
        return self.elements + other.elements

def main():
    '''Program to find if there is a subset of a list that sums to a value k
    using both the Brute Force and Ignorance(BFI) approach and the Horowitz
    and Sahni, devide and conqure approach. it counts the number of operations
    each preforms'''

    #Testing structure given by Robin Dawes.
    n_values = []
    BFI_ops_ave = []
    HS_ops_ave = []
    BFI_bigo = []
    HS_bigo = []
    for n in tqdm(range(4, 16)):  #set sizes
        BFI_res = []
        HS_res = []
        for i in range(1, 20): #20 tests per set size
            S_test = [random.randint(1,50) for x in range(n)]
            targets = [random.randint(0, 200) for y in range(10)]
            BFI_temp = []
            HS_temp = []
            for t in targets:
                BFI_temp.append(BFI_subset_sum_ops(S_test,t))
                HS_temp.append(horowitz_sahni_ops(S_test,t))
            BFI_res.append(mean(BFI_temp))
            HS_res.append(mean(HS_temp))
        n_values.append(n)
        BFI_ops_ave.append(mean(BFI_res))
        HS_ops_ave.append(mean(HS_res))
        BFI_bigo.append(2**n)
        HS_bigo.append(n*(2**(n/2)))

    plt.subplot(1, 2, 1)
    plt.plot(n_values, BFI_ops_ave, 'b', label='BFI Operations')
    plt.plot(n_values, BFI_bigo, 'r--', label='O(2^n)')
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('Operations')

    print(len(n_values))
    print(len(HS_ops_ave))

    plt.subplot(1, 2, 2)
    plt.plot(n_values, HS_ops_ave, 'b', label='h & S Operations')
    plt.plot(n_values, HS_bigo, 'r--', label='O(n*2^(n/2))')
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('Operations')
    plt.show()


def BFI_subset_sum_ops(S,k):
    '''This is an implementation of the brute force and ignorance approach to
    the subset sum problem. Structure of algorithm given by Robin Dawes in
    pseudo code. Inputs are:
    :param S: = list of elements
    :param k: = target sum
    '''
    ops = 0 #set operations counter to 0
    subsets = []
    empty_set = Set([])
    subsets.append(empty_set)


    '''Iterate through all existing subsets and create a new subset withone one
    more element from the list'''
    for element in S:
        new_subsets = []
        for old_sub in subsets:
            new_elements = old_sub.elements.copy()
            ops += 1 #copy list of elements

            #add new element to every subset creating new subset
            new_elements.append(element)
            ops += 1 #append new element to list

            new_sub = Set(new_elements)
            ops += 1#create new subset

            #check if we have found a subset that satesfies the requirements
            if new_sub.sum == k:
                return ops
            ops += 1 #comparing values

            #add new subsets to subset list
            new_subsets.append(old_sub)
            ops += 1 #moving data
            new_subsets.append(new_sub)
            ops += 1 #moving data
        subsets = new_subsets
        ops += 1 #moving data

    #if you reach the end of this loop it means there is no solution
    return ops


def horowitz_sahni_ops(S,k):
    '''This is an implementation of the Horowitz and Sahni approach to
    the subset sum problem. Structure of algorithm given by Robin Dawes in pseudo
    code. Inputs are:
    :param S: = list of elements
    :param k: = target sum
    '''
    ops = 0 #set operations counter to 0

    #split elements into left and right
    S_left = S[:len(S)//2]
    ops += 1 #accessing and moving data
    S_right = S[len(S)//2:]
    ops += 1 #accessing and moving data

    #find all subsets of these two lists
    subsets_left, ops_left= BFI_subsets_mod_ops(S_left)
    subsets_right, ops_right = BFI_subsets_mod_ops(S_right)
    ops = ops + ops_left + ops_right

    #check if there is a subset if left or right that sums to the target
    for subset in subsets_left:
        ops += 1 #comparing values
        if subset.sum == k:
            return ops
    for subset in subsets_left:
        ops += 1 #comparing values
        if subset.sum == k:
            return ops

    #sort both subset lists based on sum
    subsets_left.sort()
    ops += (3*len(subsets_left)*(math.log(len(subsets_left))))
    subsets_right.sort()
    ops += (3*len(subsets_right)*(math.log(len(subsets_right))))

    #compare pairwise sum of both left and right sets
    return pair_sum_ops(subsets_left, subsets_right, k)


def BFI_subsets_mod_ops(S):
    '''This is a modified BFI approach to the subset sum problem. It returns
    the list of subsets but not checking for a target sum. Structure of
    algorithm given by Robin Dawes in pseudo code. Inputs are:
    :param S: = list of elements
    '''
    ops = 0 #seting ops to 0
    subsets = []
    empty_set = Set([])
    subsets.append(empty_set)

    '''iterate through all existing subsets and create a new subset with one
    more element from the list'''
    for element in S:
        new_subsets = []

        for old_sub in subsets:
            new_elements = old_sub.elements.copy()
            ops += 1 #accessing old_sub

            #add new element to every subset creating new subset
            new_elements.append(element)
            ops += 1 #adding new element

            new_sub = Set(new_elements)

            #add new subsets to subset list
            new_subsets.append(old_sub)
            ops += 1 #moving data
            new_subsets.append(new_sub)
            ops += 1 #moving data

        subsets = new_subsets
        ops += 1 #moving data

    #return array of all subsets if sum not found
    return subsets, ops


def pair_sum_ops(s_left, s_right, k):
    '''pairwise sum of two sorted lists. Structure of algorithm given by
    Robin Dawes in pseudo code. Inputs are:
    :param s_left: = sorted half of full list
    :param s_right: = sorted other half of full list
    '''
    ops = 0 #set operations to 0
    i = 0
    j = len(s_right)-1

    #increment from left and right untill sum is found or one list is empty
    while i < len(s_left) and j >= 0:
        temp = s_left[i].sum + s_right[j].sum
        ops += 1 #accessing data
        ops += 1 #comparing data
        if temp == k: #check if sum equals target
            final = s_left[i] + s_right[j]
            return ops
        elif temp < k:#if too small take one higher from s_left
            i += 1
        else:#if too big take one smaller from s_right
            j -= 1
        ops += 1 #comparing data


    return ops


if __name__ == '__main__':
    main()
