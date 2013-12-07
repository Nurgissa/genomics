import fileinput
import random

def simulate_sequence(length, seed):
    random.seed(seed)
    dna = ['A', 'C', 'G', 'T', 'N']
    sequence = ''
    for i in range(length):
        sequence += random.choice(dna)
    return sequence

def read_fasta():
    snippet = ""
    for line in fileinput.input():
        #if line[0] != '>':
        snippet += line.strip()
    return [ord(char) for char in snippet]

def main():
    print read_fasta()
    pass

if __name__ == '__main__':
    main()


