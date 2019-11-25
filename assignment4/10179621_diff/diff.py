"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""
import argparse
import numpy as np
from os.path import join

class FancyString(object):
    """ this object take care of all string comparison issues.

    This is done by implementing the polynomial rolling hash function to
    increase comparison times for false comparisons.
    The __eq__ function overloads '==' to use the proper 2 step comparison
    two strings.

    Attributes:
        str (string): full string.
        f1 (int): hash assigned by function1.
    """

    def __init__(self,str):
        self.str = str
        self.f1 = FancyString.function1(str)

    def function1(str):
        """ implementation of the polynomial rolling hash function"""
        p=15485863 # fairly large prime
        m=10**9+7 # another large prime
        hash = 0
        p_pow = 1
        for char in str:
            hash = (hash + (ord(char) - ord('a') + 1) * p_pow) % m
            p_pow = (p_pow * p) % m
        return hash

    def __eq__(self, other):
        """this ensures that if hashes match then strings are checked directly
        so as not to allow false positives."""
        if self.f1 != other.f1:
            return False
        if self.str != other.str:
            return False
        return True



def main():
    """executes file comparison given user specification of file location."""
    parser = argparse.ArgumentParser(description='Use LCS algorithm to find the difference between two files.')
    parser.add_argument('-p', '--path', type=str, help='folder containing files', required=True)
    parser.add_argument('-f1','--file1', type=str, help='name of file 1', required=True)
    parser.add_argument('-f2','--file2', type=str, help='name of file 2', required=True)
    args = parser.parse_args()

    file1 = load_files(join(args.path,args.file1))
    file2 = load_files(join(args.path,args.file2))
    lcsl_matrix = lcs_matrix_builder(file1,file2)
    out = output(lcsl_matrix,args.file1,args.file2)

    print(f'{args.file1}: {lcsl_matrix.shape[0]}, {args.file2}: {lcsl_matrix.shape[1]}\n')
    for line in out:
        print(line)


def output(lcsl,file1,file2):
    """Main function that orchestrates the construction of the output.

    This function facilitatesthe building of strings by traversing the lcs
    matrix untill a line of matches turns into a line of mismatches and visa
    versa. when one is encountered this file uses match_helper and
    mismatch_helper to build the proper output strings and then stores them in
    outstrings.

    Args:
        lcsl (np.Matrix): 2-D array containing LCS information.
        file1 (string): name of the first file.
        file2 (string): name of the second file.

    Returns:
        list: list containing strings which are each a line of the desired
        output.
    """
    outstrings = []
    i = lcsl.shape[0]-1
    j = lcsl.shape[1]-1

    while i > 0 or j >0:
        val = lcsl[i,j]
        if lcsl[i-1,j] == val-1 and lcsl[i,j-1] == val-1:
            i, j, str = match_helper(lcsl,i,j,val,file1,file2)
            outstrings = [str] + outstrings

        else:
            i, j, str = mismatch_helper(lcsl,i,j,val,file1,file2)
            outstrings = [str] + outstrings

    return outstrings


def match_helper(lcsl,i,j,val,file1,file2):
    """generate output string when a match is encountered.

    This helper continues along the diagonal untill it finds a non match and
    then builds a string that represents the series of lines in each file that
    matches.

    Args:
        lcsl (np.Matrix): 2-D array containing LCS information.
        i (int): the current index in the first dimension of lcsl (file1).
        j (int): the current index in the second dimension of lcsl (file2).
        file1 (string): name of the first file.
        file2 (string): name of the second file.
    Returns:
        string: a string representing the set of matching lines.
        i, j: current indicies in lcsl.
    """
    end = (i,j)
    while lcsl[i-1,j] == val-1 and lcsl[i,j-1] == val-1:
        val = lcsl[i-1,j]
        i-=1
        j-=1
        if i == 0 or j == 0:
            break

    lines = (print_helper(i,end[0]),print_helper(j,end[1]))
    str = 'Match:         {}: {: <15}  {}: {: <15}'.format(file1,lines[0],file2,lines[1])
    return i, j, str


def mismatch_helper(lcsl,i,j,val,file1,file2):
    """generate output string when a mismatch is encountered.

    This helper continues up and to the left untill it finds a non mismatch and
    then builds a string that represents the series of lines in each file that
    matches.

    Args:
        lcsl (np.Matrix): 2-D array containing LCS information.
        i (int): the current index in the first dimension of lcsl (file1).
        j (int): the current index in the second dimension of lcsl (file2).
        file1 (string): name of the first file.
        file2 (string): name of the second file.
    Returns:
        string: a string representing the set of mismatched lines.
        i, j: current indicies in lcsl.
    """
    end = (i,j)
    while i > 0 and lcsl[i-1,j] == val:
        i-=1
        if i == 0:
            break

    while j > 0 and lcsl[i,j-1] == val:
        j-=1
        if j == 0:
            break

    lines = (print_helper(i,end[0]),print_helper(j,end[1]))
    str = 'Mismatch:      {}: {: <15}  {}: {: <15}'.format(file1,lines[0],file2,lines[1])
    return i, j, str


def print_helper(start,end):
    """change indicies of matrix back to line numbers of the original file"""

    if start == end:
        return 'None'
    else:
        if start == 0:
            return f'<{start+1} .. {end+1}>'
        else:
            return f'<{start+2} .. {end+1}>'


def lcs_matrix_builder(list1,list2):
    """Build a longest common substring using LCS algorithm provided in class.

    Args:
        list1 (list(FancyString)): first list of FancyStrings to compare.
        list2 (list(FancyString)): second list of FancyStrings to compare.

    Returns:
        np.Matrix: matrix containing LCSL information.
    """
    lcsl = np.zeros((len(list1),len(list2)))
    lcsl = base_cases(lcsl,list1,list2)

    for i in range(1,len(list1)):
        for j in range(1,len(list2)):
            if list1[i] == list2[j]:
                lcsl[i,j] = 1 + lcsl[i-1,j-1]
            else:
                lcsl[i,j] = max(lcsl[i-1,j],lcsl[i,j-1])
    return lcsl




def base_cases(matrix, list1, list2):
    """Initialize matrix with first row and collumn using base casses provided
    in class.

    Args:
        file (string): location of file.

    Returns:
        list: list containing a string for each line in the file.
    """
    if list1[0] == list2[0]:
        matrix[0,0] = 1
    else:
        matrix[0,0] = 0

    for i in range(1, len(list2)):
        if matrix[0,i-1] == 1:
            matrix[0,i] = 1
        elif list1[0] == list2[i]:
            matrix[0,i] = 1

    for i in range(1, len(list1)):
        if matrix[i-1,0] == 1:
            matrix[i,0] = 1
        elif list1[i] == list2[0]:
            matrix[i,0] = 1
    return matrix


def load_files(file):
    """load text from a file to a list of FancyString which include hashes.

    Args:
        file (string): location of file.

    Returns:
        list: list containing a FancyString for each line in the file.
    """
    with open(file) as f:
        file_l = f.readlines()

    fancy_list = []
    for line in file_l:
        fancy_list.append(FancyString(line))

    return fancy_list

if __name__ == '__main__':
    main()
