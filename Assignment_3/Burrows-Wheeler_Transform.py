#Burrows-Wheeler transform of a string and string matching
#Input: A genome string T, a query string P
#Output: All matches of P in T

import sys  
import random

#Function fo find the Burrows-Wheeler transform of a string
#arguments: a string
#return: the Burrows-Wheeler transform of the string
def bwt(s):
    n = len(s)
    m = sorted([s[i:] + s[:i] for i in range(n)])
    return ''.join([m[i][n-1] for i in range(n)])

#Function fo find the reverse Burrows-Wheeler transform of a string
#arguments: a string
#return: the reverse Burrows-Wheeler transform of the string
def reverse_bwt(s):
    n = len(s)
    table = ['' for i in range(n)]
    for i in range(n):
        table = sorted([s[i] + table[i] for i in range(n)])
    return table[s.index('$')]

#Function to find the suffix array of a string
def suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])

#Function to find the maching of the query string in the genome string
#arguments: genome string, query string
#return: the number of matches of the query string in the genome string
def bwt_matching(genome, query):
    first_col = ''.join(sorted(genome))
    last_col = bwt(genome)
    top = 0
    bottom = len(last_col) - 1
    while top <= bottom:
        if query:
            symbol = query[-1]
            query = query[:-1]
            if symbol in last_col[top:bottom+1]:
                top = first_col.find(symbol) + last_col[:top].count(symbol)
                bottom = first_col.find(symbol) + last_col[:bottom+1].count(symbol) - 1
            else:
                return 0
        else:
            return bottom - top + 1
        
#Function to report the offset in the genome string of each match
#arguments: genome string, query string
#return: the offset of each match of the query string in the genome string
def bwt_matching_positions(genome, query):
    first_col = ''.join(sorted(genome))
    last_col = bwt(genome)
    top = 0
    bottom = len(last_col) - 1
    positions = []
    while top <= bottom:
        if query:
            symbol = query[-1]
            query = query[:-1]
            if symbol in last_col[top:bottom+1]:
                top = first_col.find(symbol) + last_col[:top].count(symbol)
                bottom = first_col.find(symbol) + last_col[:bottom+1].count(symbol) - 1
            else:
                return []
        else:
            for i in range(top, bottom + 1):
                positions.append(suffix_array(genome)[i])
            return sorted(positions)

# Function to generate a random nucleotide sequence of given length
def generate_random_sequence(length):
    return ''.join(random.choices('ACGT', k=length))

# Function to insert a pattern into a sequence at a random position
def insert_pattern(sequence, pattern):
    position = random.randint(0, len(sequence))
    return sequence[:position] + pattern + sequence[position:]

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python3 Burrows-Wheeler_Transform.py")
        sys.exit(1)
    
    T = generate_random_sequence(20)

    P1 = generate_random_sequence(5)
    while P1 in T:
        P1 = generate_random_sequence(5)
    T_with_P1 = insert_pattern(T, P1)

    P2 = generate_random_sequence(5)
    while P2 in T_with_P1:
        P2 = generate_random_sequence(5) 
    T_with_P1_P2 = insert_pattern(T_with_P1, P2)
    T_with_P1_P2 = insert_pattern(T_with_P1_P2, P2)

    P3 = generate_random_sequence(5)
    while P3 in T_with_P1_P2:
        P3 = generate_random_sequence(5)

    # Verify the matches
    matches_P1 = bwt_matching_positions(T_with_P1_P2, P1)
    matches_P2 = bwt_matching_positions(T_with_P1_P2, P2)
    matches_P3 = bwt_matching_positions(T_with_P1_P2, P3)

    print(f"Sequence T: {T_with_P1_P2}")
    print(f"P1: {P1}")
    print(f"P2: {P2}")
    print(f"P3: {P3}")

    print(f"Matches for P1: {matches_P1}")
    print(f"Matches for P2: {matches_P2}")
    print(f"Matches for P3: {matches_P3}")