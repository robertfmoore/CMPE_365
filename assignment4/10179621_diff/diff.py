"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""
import argparse
import numpy as np
from os.path import join


def main():
    """executes encoding given user specifications."""
    parser = argparse.ArgumentParser(description='Use LCS algorithm to find the difference between two files.')
    parser.add_argument('-p', '--path', type=str, help='folder containing files', required=True)
    parser.add_argument('-f1','--file1', type=str, help='name of file 1', required=True)
    parser.add_argument('-f2','--file2', type=str, help='name of file 2', required=True)
    args = parser.parse_args()

    file1 = load_files(join(args.path,args.file1))
    file2 = load_files(join(args.path,args.file2))

    lcsl_matrix = lcs_matrix_builder(file1,file2)
    print(f'{args.file1}: {lcsl_matrix.shape[0]}, {args.file2}: {lcsl_matrix.shape[1]}')

    out = output(lcsl_matrix,args.file1,args.file2)

    for line in out:
        print(line)


def output(lcsl,file1,file2):
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
    if start == end:
        return 'None'
    else:
        if start == 0:
            return f'<{start+1} .. {end+1}>'
        else:
            return f'<{start+2} .. {end+1}>'


def lcs_matrix_builder(list1,list2):
    """load text from a file to a list of strings.

    Args:
        file (string): location of file.

    Returns:
        list: list containing a string for each line in the file.
    """
    lcsl = np.zeros((len(list1),len(list2)))
    lcsl = base_cases(lcsl,list1,list2)

    for i in range(1,len(list1)):
        for j in range(1,len(list2)):
            if check(list1[i],list2[j]):
                lcsl[i,j] = 1 + lcsl[i-1,j-1]
            else:
                lcsl[i,j] = max(lcsl[i-1,j],lcsl[i,j-1])
    return lcsl




def base_cases(matrix, list1, list2):
    """load text from a file to a list of strings.

    Args:
        file (string): location of file.

    Returns:
        list: list containing a string for each line in the file.
    """
    if check(list1[0],list2[0]):
        matrix[0,0] = 1
    else:
        matrix[0,0] = 0

    for i in range(1, len(list2)):
        if matrix[0,i-1] == 1:
            matrix[0,i] = 1
        elif check(list1[0],list2[i]):
            matrix[0,i] = 1

    for i in range(1, len(list1)):
        if matrix[i-1,0] == 1:
            matrix[i,0] = 1
        elif check(list1[i],list2[0]):
            matrix[i,0] = 1
    return matrix


def check(string1, string2):
    """compare two strings for equality.

    strings are compared by checking hashes and if both agree double check
    by comparing actual strings.

    Args:
        string1 (string): first string to compare.
        string2 (string):second string to compare.

    Returns:
        Boolean: True is strings are the same, False if they are diferent.

    """
    if string1==string2:
        return True
    return False






def load_files(file):
    """load text from a file to a list of strings.

    Args:
        file (string): location of file.

    Returns:
        list: list containing a string for each line in the file.
    """
    with open(file) as f:
        file_l = f.readlines()

    return file_l

if __name__ == '__main__':
    main()
