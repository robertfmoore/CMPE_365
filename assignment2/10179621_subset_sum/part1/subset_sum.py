"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""
import argparse

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
    and Sahni, devide and conqure approach.'''

    parser = argparse.ArgumentParser(description='determine a subset of elements in a list that sum to a target.')
    parser.add_argument('-t','--target', type=int, help='desired sum of subsets')
    parser.add_argument('-l','--list', nargs='+', type=int, help='list of elements')

    args = parser.parse_args()
    S = args.list
    k = args.target

    print(f'BFI found : {BFI_subset_sum(S,k)}')
    print(f'Horowitz & Sahni found : {horowitz_sahni(S,k)}')


def BFI_subset_sum(S,k):
    '''This is an implementation of the brute force and ignorance approach to
    the subset sum problem. Structure of algorithm given by Robin Dawes in
    pseudo code. Inputs are:
    :param S: = list of elements
    :param k: = target sum
    '''

    subsets = []
    empty_set = Set([])
    subsets.append(empty_set)


    '''Iterate through all existing subsets and create a new subset withone one
    more element from the list'''
    for element in S:
        new_subsets = []
        for old_sub in subsets:
            new_elements = old_sub.elements.copy()
            #add new element to every subset creating new subset
            new_elements.append(element)
            new_sub = Set(new_elements)

            #check if we have found a subset that satesfies the requirements
            if new_sub.sum == k:
                return new_sub.elements
            #add new subsets to subset list
            new_subsets.append(old_sub)
            new_subsets.append(new_sub)
        subsets = new_subsets

    #if you reach the end of this loop it means there is no solution
    return 'no subset sums to target value'


def horowitz_sahni(S,k):
    '''This is an implementation of the Horowitz and Sahni approach to
    the subset sum problem. Structure of algorithm given by Robin Dawes in pseudo
    code. Inputs are:
    :param S: = list of elements
    :param k: = target sum
    '''
    #split elements into left and right
    S_left = S[:len(S)//2]
    S_right = S[len(S)//2:]

    #find all subsets of these two lists
    subsets_left = BFI_subsets_mod(S_left)
    subsets_right = BFI_subsets_mod(S_right)

    #check if there is a subset if left or right that sums to the target
    for subset in subsets_left:
        if subset.sum == k:
            return subset.elements
    for subset in subsets_left:
        if subset.sum == k:
            return subset.elements

    #sort both subset lists based on sum
    subsets_left.sort()
    subsets_right.sort()

    #compare pairwise sum of both left and right sets
    return pair_sum(subsets_left, subsets_right, k)


def BFI_subsets_mod(S):
    '''This is a modified BFI approach to the subset sum problem. It returns
    the list of subsets but not checking for a target sum. Structure of
    algorithm given by Robin Dawes in pseudo code. Inputs are:
    :param S: = list of elements
    '''

    subsets = []
    empty_set = Set([])
    subsets.append(empty_set)

    '''iterate through all existing subsets and create a new subset with one
    more element from the list'''
    for element in S:
        new_subsets = []
        for old_sub in subsets:
            new_elements = old_sub.elements.copy()
            #add new element to every subset creating new subset
            new_elements.append(element)
            new_sub = Set(new_elements)

            #add new subsets to subset list
            new_subsets.append(old_sub)
            new_subsets.append(new_sub)

        subsets = new_subsets

    #return array of all subsets if sum not found
    return subsets


def pair_sum(s_left, s_right, k):
    '''pairwise sum of two sorted lists. Structure of algorithm given by
    Robin Dawes in pseudo code. Inputs are:
    :param s_left: = sorted half of full list
    :param s_right: = sorted other half of full list
    '''
    i = 0
    j = len(s_right)-1

    #increment from left and right untill sum is found or one list is empty
    while i < len(s_left) and j >= 0:
        temp = s_left[i].sum + s_right[j].sum
        if temp == k: #check if sum equals target
            final = s_left[i] + s_right[j]
            return final
        elif temp < k:#if too small take one higher from s_left
            i += 1
        else:#if too big take one smaller from s_right
            j -= 1

    return 'no subset sums to target value'


if __name__ == '__main__':
    main()
