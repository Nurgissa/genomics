import fileinput
import random

def simulate_sequence(length, seed):
    """
    TO-DO:
    """
    random.seed(seed)
    dna = ['A', 'C', 'G', 'T', 'N']
    sequence = ''
    for i in range(length):
        sequence += random.choice(dna)
    return sequence

def read_fasta():
    """
    TO-DO:
    """
    sequence = ""
    for line in fileinput.input():
        #if line[0] != '>':
        sequence += line.strip()
    print "File was loaded.\n "
    return sequence

def convert_to_int(my_string):
    """
    TO-DO:
    """
    return [ord(char) for char in my_string]


def main():
    pass

if __name__ == '__main__':
    main()


