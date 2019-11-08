"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""
import argparse
from collections import Counter
from heapq import *

def main():
    """executes encoding given user specifications."""
    parser = argparse.ArgumentParser(description='generate code strings given a collection of text using Huffman coding.')
    parser.add_argument('-i','--in_file', type=str, help='file to encode', required=True)
    parser.add_argument('-e','--encoding', type=str, help='encoding file', required=True)
    parser.add_argument('-o','--out_file', type=str, help='save encoded file', required=True)
    args = parser.parse_args()

    encoding = load_encoding(args.encoding)
    clear_text = load_file(args.in_file)
    ascii_chars = char_to_ascii(clear_text)
    encoded_text = huffman_encode(ascii_chars, encoding)
    save_file(encoded_text, args.out_file)

def huffman_encode(ascii_chars, encoding):
    """Encodes chars based on encoding.

    Args:
        ascii_chars (list(int)): Ordered list of all chars to encode.
        encoding (dictionary): dictionary defining huffman code to encode with.

    Returns:
        string: string of encoded 'bits' represented as '1' and '0'.
    """
    code_string = ''

    for char in ascii_chars:
        code_string += encoding[char]

    return code_string

def char_to_ascii(char_list):
    """convert a list of characters to a list of respective ascii values"""
    ascii_list = [ord(char) for char in char_list]
    return ascii_list


def load_encoding(file_name):
    """load canonical collection of text from a file.

    Args:
        file_name (string): Location of file containing huffman code.

    Returns:
        dictionary: dictionary defined as {ascii_value:huffman_code(string)}.
    """
    with open(file_name) as f:
        file = f.readlines()

    encoding ={}
    for line in file:
        x = line.split()
        encoding.update({int(x[0]):x[1]})

    return encoding

def load_file(file_name):
    """load text from a file to a list of characters.

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

def save_file(content, file_name):
    """save content content to file_name"""
    with open(file_name,'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()
