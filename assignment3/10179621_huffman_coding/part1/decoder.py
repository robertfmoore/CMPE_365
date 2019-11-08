"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""
import argparse
from collections import Counter
from heapq import *
from code_building import HuffmanNode
from encoder import save_file

def main():
    '''
    Program to acurately decode a simulated binary huffman encoded file. This
    decoding program decodes using an efficient implementation using a huffman
    tree.
    '''
    parser = argparse.ArgumentParser(description='generate code strings given a collection of text using Huffman coding.')
    parser.add_argument('--in_file', '-i', type=str, help='file to decode', required=True)
    parser.add_argument('--encoding', '-e', type=str, help='encoding file',required=True)
    parser.add_argument('--out_file', '-o', type=str, help='save decoded file',required=True)
    args = parser.parse_args()

    encoding = load_encoding(args.encoding)
    encoded_text = load_file(args.in_file)
    chars_tree = tree_decoder(encoded_text, encoding)
    clear_text = ascii_to_char(chars_tree)
    save_file(clear_text, args.out_file)

def build_huff_tree(huffman_dict):
    ''' This function initiates tree_helper() to reconstruct the original
    huffman tree from the inverted encoding dictionary.

    Args:
        huffman_dict (dictionary): inverted encoding dictionary
        {code: ascii_code}.
    Returns:
        HuffmanNode: root node of complete Huffman Tree.
    '''
    code = ''
    node = HuffmanNode()
    tree = tree_helper(huffman_dict, node, code)
    return tree #root node of huffman tree

def tree_helper(huffman_dict, node, code):
    """Recursively calls itself untill full subtree is built.

    Args:
        huffman_dict (dictionary): inverted encoding dictionary
        {code: ascii_code}.
        node (HuffmanNode): current node of tree.
        code (string): code up to current node.

    Returns:
        HuffmanNode: current node if code is in huffman_dict or full subtree
        with current node as root.
    """
    if code in huffman_dict:
        node.value = huffman_dict.pop(code)

    else:
        node.zero = tree_helper(huffman_dict, HuffmanNode(), code+'0')
        node.one = tree_helper(huffman_dict, HuffmanNode(), code+'1')

    return node

def tree_decoder(encoded_text, decoding_dict):
    """Decodes encoded_text using decoding_dict.

    This implementation efficiently decodes encoded text in O(n) time by
    utilizing the reconstructed huffman tree and traversing it untill a leaf
    node is found.

    Args:
        encoded_text (string): string of '1' and '0' representing bits.
        decoding_dict (dictionary): inverted encoding dictionary
        {code: ascii_code}.

    Returns:
        list(int): list of ascii values of decoded characters.
    """
    root = build_huff_tree(decoding_dict) #reconstruct huffman tree from dict.
    node = root
    ascii_list = []
    for i in range(len(encoded_text)):
        if encoded_text[i] == '0':
            node = node.zero
        else:
            node = node.one
        #if node is a leaf node, add value to decoded text and restart at root.
        if node.value is not None:
            ascii_list.append(node.value)
            node = root

    return ascii_list

def huffman_decode(encoded_text, decoding_dict):
    """this is a simple implementation to check that decoding is working.

    *very inefficient* so it is not used
    """
    ascii_list = []
    tmp = ''
    for i in range(len(encoded_text)):
        tmp += encoded_text[i]
        if tmp in decoding_dict:
            ascii_list.append(decoding_dict[tmp])
            tmp = ''

    return ascii_list

def ascii_to_char(ascii_list):
    """convert a list of ascii values to a list of respective characters"""
    text = ''
    for num in ascii_list:
        text += chr(num)
    return text


def load_encoding(file_name):
    """load canonical collection of text from a file

    Args:
        file_name (string): location of saved encoding.

    Returns
        dictionary: inverted encoding dictionary
        {code: ascii_code}.
    """

    with open(file_name) as f:
        file = f.readlines()

    encoding ={}
    for line in file:
        x = line.split()
        encoding.update({x[1]:int(x[0])})

    return encoding


def load_file(file_name):
    """load encoded string of '1' adn '0' from a file

    Args:
        file_name (string): location of file.

    Returns:
        string: full string text in file_name.
    """

    with open(file_name) as f:
        file = f.readline()
    return file

if __name__ == '__main__':
    main()
