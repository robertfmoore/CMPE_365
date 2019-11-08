"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""
import argparse
from collections import Counter
from heapq import *
import glob
from tqdm import tqdm


class HuffmanNode(object):
    """This class is used for constructing and decoding Huffman Codes.

    Attributes:
        freq (int): Frequency or number of occurances of current nodes.
        value (int): ASCII code associated to node if self is leaf nodes.
        zero (HuffmanNode): Node with the same code appended with a zero.
        one (HuffmanNode): Node with the same code appended with a one.
    """

    def __init__(self, freq=None, value=None, zero=None, one=None):
        """Initialize HuffmanNode with all Attributes defaulted to None."""

        self.freq = freq
        self.value = value
        self.zero = zero
        self.one = one

    def gen_code(self,pre_code=''):
        """Generate huffman code for all nodes in subtree.

        This generate the full huffman code when run on the root node of the
        huffman tree.

        Args:
            pre_code (string): code prefix up to current node.
        Returns:
            dictionary : dictionary of full huffman code for subtree with
            current node as root and prefixed with pre_code.
        """
        if self.value:
            return {self.value:pre_code}
        dic = self.zero.gen_code(pre_code +'0')
        dic.update(self.one.gen_code(pre_code + '1'))
        return dic

    def __lt__(self, other):
        """Compares one HuffmanNode to another based on their frequency (freq).

        Args:
            other (HuffmanNode): Node to compare to.
        """
        return self.freq < other.freq

    def __add__(self, other):
        """Adds other (HuffmanNode) to current node.

        Nodes are added by adding each frequency and creating new HuffmanNode
        with this frequency and no value.

        Args:
            other (HuffmanNode): Node to add to current Node.

        Returns:
            HuffmanNode: Node with frequency equal to sum of self node and other
            node.
        """
        tmp_freq = self.freq + other.freq
        return HuffmanNode(tmp_freq, zero=self, one=other)


def main():
    #collecting arguments from user.
    """IMPORTANT for glob functionality in_file must be passed as a string"""
    parser = argparse.ArgumentParser(description='generate code strings given a collection of text using Huffman coding.')
    parser.add_argument('-i', '--in_file', type=str, help='glob string containing files for building code' , required=True)
    parser.add_argument('-o', '--out_file', type=str, default='encoding.txt', required=True)
    args = parser.parse_args()

    #Build huffman code based on inputs specified by user.
    #modified to take more than one file.
    all_chars = []
    for file in tqdm(glob.glob(args.in_file)):
        all_chars = load_collection(file)

    ascii_chars = char_to_ascii(all_chars)
    char_freq = printable_char_freq(ascii_chars)
    encoding = Huffman_encoding(char_freq.most_common())
    save_code(encoding, args.out_file)


def Huffman_encoding(char_freq):
    """Generate Huffman Code given character frequencies.

    This generation method implements a binary Huffman Tree for code generation.

    Args:
        char_freq (dictionary): dictionary defined as
        {ascii_value: occurances/frequency}.

    Returns:
        dictionary: dictionary defined as {ascii_value:huffman_code(string)}.
    """
    nodes = [HuffmanNode(freq=x[1],value=x[0]) for x in char_freq]
    heapify(nodes)
    #iterate until only one node remains. this node is the root of the hufftree.
    while len(nodes)>1:
        node_1 = heappop(nodes)
        node_2 = heappop(nodes)
        tmp = node_1 + node_2
        heappush(nodes,tmp)

    root = heappop(nodes) #this is the root of the huffman tree
    return root.gen_code() # generates entire huffman code.


def printable_char_freq(char_list):
    """Counts the # of occurences of each printable ascii charater.

    Args:
        char_list (list(int)): List of ascii values.
    Returns:
        dictionary: dictionary defined as {ascii_value: #_of_occurances}.
    """
    char_count = Counter({x:0 for x in range(32,127)})
    char_count[10]=0
    for char in tqdm(char_list):
        char_count[char] += 1
    return char_count

def char_to_ascii(char_list):
    """returns a list ascii values coresponding to list of characters."""
    ascii_list = [ord(char) for char in char_list]
    return ascii_list


def load_collection(file_name):
    """load canonical collection of text from a file

    Args:
        file_name (string): location of file.

    Returns:
        list: list containing all characters in file_name.
    """
    all_chars = []
    with open(file_name) as f:
        file = f.readlines()

    for line in file:
            all_chars = all_chars + [char for char in line]

    return all_chars

def save_code(huff_code, out_file):
    """Saves dictionary containing huff_code to out_file.

    code is saved as:
    key1 value1
    key2 value2
    ...

    Args:
        huff_code (dictionary): dictionary defined as
        {ascii_value:huffman_code(string)}.
        out_file (string): location to save huffman code
    """
    with open(out_file, 'w') as f:
        for char, code in huff_code.items():
            f.write(f'{char} {code}\n')


if __name__ == '__main__':
    main()
